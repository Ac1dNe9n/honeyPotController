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

RUN apt -y update \
 && apt -y upgrade \
 && DEBIAN_FRONTEND=noninteractive \
 apt -y install \
 wget \
 curl \
 git \
 htop \
 net-tools \
 iputils-ping \
 iptables \
 \
 && echo "root:root" | chpasswd

# RUN rm -rf /var/lib/apt/lists/*


