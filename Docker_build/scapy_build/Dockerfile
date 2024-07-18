FROM docker.io/ubuntu:24.04

RUN apt-get update ; apt-get install -y python3-scapy iproute2 && \
rm -rf /var/lib/apt/lists/* && apt-get clean && mkdir /root/scapy_scripts

WORKDIR /root/scapy_scripts
EXPOSE 53 53/udp
CMD ["bash"]
