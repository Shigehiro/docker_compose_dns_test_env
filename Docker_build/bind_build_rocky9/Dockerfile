FROM rockylinux:9
LABEL maintainer Shiehiro Hattori <narihiro.h@gmail.com>

ARG BIND_VERSION=9.16.23-1.el9

RUN dnf update -y && dnf install -y bash-completion iproute which man \
  bind-$BIND_VERSION \
  bind-dnssec-doc-$BIND_VERSION \
  bind-dnssec-utils-$BIND_VERSION \
  bind-libs-$BIND_VERSION \
  bind-license-$BIND_VERSION \
  bind-utils-$BIND_VERSION \
  python3-bind-$BIND_VERSION && sh /usr/libexec/generate-rndc-key.sh && dnf clean all && rm -rf /var/cache/yum 

VOLUME ["/etc/named", "/var/named/data", "/run/named"]

WORKDIR /root

CMD ["/usr/sbin/named", "-g", "-u", "named", "-c", "/etc/named.conf", "-4", "-d", "100"]
