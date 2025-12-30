#!/bin/bash

R1="clab-two-router-bgp-r1"
INTERFACE="eth1"
SLEEP_DOWN=5
SLEEP_UP=5

while true; do
  echo "[$(date)] Bringing BGP link DOWN"
  docker exec $R1 ip link set $INTERFACE down
  sleep $SLEEP_DOWN

  echo "[$(date)] Bringing BGP link UP"
  docker exec $R1 ip link set $INTERFACE up
  sleep $SLEEP_UP
done
