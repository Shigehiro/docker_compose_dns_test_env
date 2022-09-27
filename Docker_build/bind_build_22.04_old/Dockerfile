FROM ubuntu:jammy

ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8

ARG DEB_VERSION=1:9.18.1-1ubuntu1

# Install BIND 9
RUN apt-get -qqqy update
RUN apt-get -qqqy dist-upgrade
RUN apt-get -qqqy install bind9=$DEB_VERSION bind9-utils=$DEB_VERSION bind9-libs=$DEB_VERSION
RUN apt-get -qqqy install bind9-dnsutils nftables

RUN mkdir -p /etc/bind && chown root:bind /etc/bind/ && chmod 755 /etc/bind
RUN mkdir -p /var/cache/bind && chown bind:bind /var/cache/bind && chmod 755 /var/cache/bind
RUN mkdir -p /var/lib/bind && chown bind:bind /var/lib/bind && chmod 755 /var/lib/bind
RUN mkdir -p /var/log/bind && chown bind:bind /var/log/bind && chmod 755 /var/log/bind
RUN mkdir -p /run/named && chown bind:bind /run/named && chmod 755 /run/named && rm -f /etc/nftables.conf

VOLUME ["/etc/bind", "/var/cache/bind", "/var/lib/bind", "/var/log"]

ADD ./nftables.conf /etc/nftables.conf
ADD ./entrypoint.sh /usr/sbin/entrypoint.sh
RUN chmod u+x /usr/sbin/entrypoint.sh

EXPOSE 53/udp 53/tcp 953/tcp

ENTRYPOINT ["entrypoint.sh"]

