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

import re
import time
import datetime
import subprocess

from log import Log


class Monitor(object):

    WAIT = 300
    RE_BYTES = '(\d+) netactivity  tcp'
    CMD_INPUT = 'iptables --list INPUT --verbose --exact'
    CMD_OUTPUT = 'iptables --list OUTPUT --verbose --exact'

    def _get_counter(self, cmd):
        raw = subprocess.check_output(cmd, shell=True)
        match = re.search(self.RE_BYTES, raw)
        return int(match.groups(0)[0])

    def _get_timestamp(self):
        return int(time.mktime(datetime.date.today().timetuple()))

    def run(self):
        log = Log()

        # use current counters as reference, dont bother with the past
        prev_download = self._get_counter(self.CMD_INPUT)
        prev_upload = self._get_counter(self.CMD_OUTPUT)

        while True:
            # check what we have now
            timestamp = self._get_timestamp()
            download = self._get_counter(self.CMD_INPUT)
            upload = self._get_counter(self.CMD_OUTPUT)

            # find the deltas
            delta_download = download - prev_download
            delta_upload = upload - prev_upload

            print timestamp, delta_download, delta_upload
            log.save(timestamp, delta_download, delta_upload)

            prev_download = download
            prev_upload = upload
            time.sleep(self.WAIT)
