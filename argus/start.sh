#!/bin/sh
if [ $RUN_MODE = "import_pcap" ]
then
    echo "MODE import_pcap"
    echo Processing $TCPDUMP_OUTPUT
    argus -f -r $TCPDUMP_OUTPUT -F /etc/argus.conf -w - | ra -F /etc/ra.conf -L -1 -r - > $ARGUS_OUTPUT
elif [ $RUN_MODE = "sniff" ]
then
    echo "MODE sniff"
    argus -i $INTERFACE -F /etc/argus.conf -w - | ra -F /etc/ra.conf -L -1 -r - > $ARGUS_OUTPUT
    tail -f /dev/null
else
  echo "Invalid mode $RUN_MODE"
fi