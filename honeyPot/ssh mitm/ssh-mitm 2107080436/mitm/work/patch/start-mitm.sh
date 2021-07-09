#!/bin/bash

chown -R ssh-mitm:ssh-mitm /work/ip2key

chmod +x /work/ssh-mitm-2.2/start.sh
/work/ssh-mitm-2.2/start.sh

chmod +x /work/ssh-mitm-2.2/JoesAwesomeSSHMITMVictimFinder.py
/work/ssh-mitm-2.2/JoesAwesomeSSHMITMVictimFinder.py --interface eth0 --listen-time 6000