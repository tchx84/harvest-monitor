# Copyright (c) 2014 Martin Abente Lahaye. - tch@sugarlabs.org
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import sqlite3


class Log(object):

    DB_PATH = '/opt/harvest-monitor/db'

    QUERY_CREATE = 'CREATE TABLE IF NOT EXISTS '\
                   'counters '\
                   '(timestamp INT PRIMARY KEY, '\
                   'download INT, '\
                   'upload INT)'

    QUERY_FIND_ONE = 'SELECT * FROM counters WHERE timestamp=?'

    QUERY_FIND_ALL = 'SELECT * FROM counters WHERE '\
                     'timestamp >= ? AND timestamp <= ?'

    QUERY_INSERT = 'INSERT OR REPLACE INTO counters '\
                   '(timestamp, download, upload) '\
                   'VALUES (?, ?, ?)'

    def __init__(self):
        self._connection = sqlite3.connect(self.DB_PATH)
        self._setup_tables()

    def _setup_tables(self):
        cursor = self._connection.cursor()
        cursor.execute(self.QUERY_CREATE)

    def find(self, start, end):
        cursor = self._connection.cursor()
        cursor.execute(self.QUERY_FIND_ALL, (start, end,))
        return cursor.fetchall()

    def save(self, timestamp, delta_download, delta_upload):
        cursor = self._connection.cursor()
        cursor.execute(self.QUERY_FIND_ONE, (timestamp,))
        counters = cursor.fetchone()

        if counters is not None:
            total_download = counters[1]
            total_upload = counters[2]
        else:
            total_download = 0
            total_upload = 0

        download = total_download + delta_download
        upload = total_upload + delta_upload

        cursor.execute(self.QUERY_INSERT, (timestamp, download, upload,))
        self._connection.commit()
