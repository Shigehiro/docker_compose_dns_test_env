FROM almalinux/8-init:latest
ADD cacheserve-7.7.0.2-378215-rhel-8-x86_64.tar.gz /tmp/
COPY channel.conf /etc/
WORKDIR /tmp
RUN rpm -ivh cacheserve-*/*.rpm \
&& echo "PATH=$PATH:/usr/local/nom/sbin:/usr/local/nom/bin" |  tee -a /root/.bashrc \
&& dnf install -y bind-utils rsyslog less man bash-completion net-tools net-snmp net-snmp-utils iproute iputils python3 \
&& echo "MANDATORY_MANPATH  /usr/local/nom/man" | tee -a /etc/man_db.conf \
dnf clean all && rm -rf /tmp/cacheserve* && systemctl enable snmpd.service && systemctl enable snmptrapd.service
#ADD nomcc /tmp/nomcc
#WORKDIR /tmp/nomcc
#RUN python3 setup.py install
COPY cacheserve.license /usr/local/nom/etc
COPY rsyslog.conf /etc
COPY snmpd.conf /etc/snmp
COPY snmp.conf /etc/snmp
COPY snmptrapd.conf /etc/snmp
COPY snmpagent.conf /etc
EXPOSE 53 53/udp 9434 853 443 161/udp 162/udp
WORKDIR /root

CMD ["/sbin/init"]
