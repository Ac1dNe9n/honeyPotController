#!/bin/bash

chmod +x /work/ssh-mitm-2.2/stop.sh
/work/ssh-mitm-2.2/stop.sh

cd /work/ssh-mitm-2.2/openssh-7.5p1-mitm
make uninstall
make clean
make install-nokeys

mv /usr/local/sbin/sshd /home/ssh-mitm/bin/sshd_mitm
