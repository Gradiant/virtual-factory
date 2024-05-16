#!/bin/sh
if [ $RUN_MODE = "sniff" ]
then
    tcpdump -i $INTERFACE -s 0 -U -n -w $TCPDUMP_OUTPUT
else
    tail -F /dev/null
fi