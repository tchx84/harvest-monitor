#!/bin/bash

# exit if already created
/usr/sbin/iptables -L | grep harvest
if [ $? -eq 0 ]; then
    exit 0
fi
 
# create our new chains to monitor
/usr/sbin/iptables -N harvest_in
/usr/sbin/iptables -N harvest_out
 
# simple return bypass
/usr/sbin/iptables -I harvest_in -j RETURN
/usr/sbin/iptables -I harvest_out -j RETURN
 
# send only interesting traffic to the bypass
/usr/sbin/iptables -I INPUT 1 ! -i lo -p tcp -m tcp ! --tcp-flags FIN,SYN,RST,ACK SYN -j harvest_in
/usr/sbin/iptables -I OUTPUT 1 ! -o lo -p tcp -m tcp ! --dport 5353 -j harvest_out
