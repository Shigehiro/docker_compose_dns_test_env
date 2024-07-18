FROM docker.io/ubuntu:latest
WORKDIR /root
RUN apt-get update && apt-get install -y tcpdump bind9-dnsutils nftables && rm -f /etc/nftables.conf

ADD ./nftables.conf /etc/nftables.conf
ADD ./entrypoint.sh /usr/sbin/entrypoint.sh
RUN chmod u+x /usr/sbin/entrypoint.sh

#EXPOSE 53/udp 53/tcp 953/tcp

ENTRYPOINT ["entrypoint.sh"]
