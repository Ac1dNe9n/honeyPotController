FROM ubuntu:18.04

# ADD ~/.inputrc ~/.inputrc
ADD sources/aliyun_sources.list /etc/apt/sources.list

RUN apt -y update \
 && apt -y install \
 dialog \
 && apt -y install \
 ca-certificates \
 apt-transport-https

ADD sources/tsinghua_sources.list /etc/apt/sources.list

WORKDIR /work/
ADD work/ssh-mitm-2.2.tar.gz /work/

RUN apt -y update \
 && apt -y upgrade \
 && DEBIAN_FRONTEND=noninteractive \
 apt -y install \
 wget \
 curl \
 git \
 htop \
 screen \
 python3 \
 python3-netaddr python3-netifaces \
 nmap ettercap-text-only tshark iptables \
 \
 && cd ssh-mitm-2.2 \
 && ./install.sh

ENV MAXMITMIP=5

ADD work/patch /work/ssh-mitm-2.2
RUN cd ssh-mitm-2.2\
 && ./zimarntPatch.sh

RUN rm -rf /var/lib/apt/lists/*


