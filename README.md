# 1. Docker Compose Set up DNS testing environment

- [1. Docker Compose Set up DNS testing environment](#1-docker-compose-set-up-dns-testing-environment)
- [2. Description](#2-description)
- [3. How to run docker-compose](#3-how-to-run-docker-compose)
- [4. About DNS Domains configured by this compose file](#4-about-dns-domains-configured-by-this-compose-file)
- [5. Dig output](#5-dig-output)
- [6. About Caching Name Servers](#6-about-caching-name-servers)
- [7. About BIND Caching Name Server](#7-about-bind-caching-name-server)
- [8. Send `www.foobar.loop` to unbound from dig-client](#8-send-wwwfoobarloop-to-unbound-from-dig-client)
- [9. About Docker host](#9-about-docker-host)

# Note

At the moment, I struggle to start unbound container.
unbound container failed to start. I will check this later.
So I have disabled starting unbound container.

# 2. Description

- set up caching name servers, such as BIND, unbound
- set up authoritative name servers with BIND
  - one internal root server, two .com, two example.com
- set up broken auth name servers with python scapy

# 3. How to run docker-compose

```text
docker-compose build
docker-compose up -d
```

# 4. About DNS Domains configured by this compose file

- *.example.com domain
  - BIND auth servers return answers for this domain
- *.scapy domain
  - scapy faked auth servers return queries for *.scpay domain, such as a.foo.capy, b.bar.scapy, c.foobar.scapy, whatever queries ended with *.scapy
- *.loop domain
  - scapy faked auth servers return infinite loop delegations
  - whatever queries ended with *.loop

# 5. Dig output

dig to *.example.com from a dig-client
```text
# dig to a root server
$ docker exec dig-client dig @172.20.0.30 www.example.com +norec +noall +answer +auth +add
com.                    3600    IN      NS      ns02.com.
com.                    3600    IN      NS      ns01.com.
ns02.com.               3600    IN      A       172.20.0.41
ns01.com.               3600    IN      A       172.20.0.40

# dig to .com server
$ docker exec dig-client dig @172.20.0.40 www.example.com +norec +noall +answer +auth +add
example.com.            3600    IN      NS      ns02.example.com.
example.com.            3600    IN      NS      ns01.example.com.
ns02.example.com.       3600    IN      A       172.20.0.51
ns01.example.com.       3600    IN      A       172.20.0.50

# dig to example.com server
$ docker exec dig-client dig @172.20.0.50 www.example.com +norec +noall +answer +auth +add
www.example.com.        3600    IN      A       1.1.1.1
```

dig to *.scapy from a dig-client
```text
# dig to a root server
$ docker exec dig-client dig @172.20.0.30 www.example.scapy +norec +noall +answer +auth +add
scapy.                  3600    IN      NS      ns01.scapy.
scapy.                  3600    IN      NS      ns02.scapy.
ns02.scapy.             3600    IN      A       172.20.0.61
ns01.scapy.             3600    IN      A       172.20.0.60

# dit to .scapy server(faked auth servers)
$ docker exec dig-client dig @172.20.0.60 www.example.scapy +norec +noall +answer +auth +add
example.scapy.          1800    IN      NS      ns01.example.scapy.
example.scapy.          1800    IN      NS      ns02.example.scapy.
ns01.example.scapy.     1800    IN      A       172.20.0.62
ns02.example.scapy.     1800    IN      A       172.20.0.63

# dig to example.scapy server(faked auth server)
$ docker exec dig-client dig @172.20.0.62 www.example.scapy +norec +noall +answer +auth +add
www.example.scapy.      1800    IN      A       1.1.1.1

# try another domain, www.foo.scapy
$ docker exec dig-client dig @172.20.0.60 www.foo.scapy +norec +noall +answer +auth +add
foo.scapy.              1800    IN      NS      ns01.foo.scapy.
foo.scapy.              1800    IN      NS      ns02.foo.scapy.
ns01.foo.scapy.         1800    IN      A       172.20.0.62
ns02.foo.scapy.         1800    IN      A       172.20.0.63

$ docker exec dig-client dig @172.20.0.63 www.foo.scapy +norec +noall +answer +auth +add
www.foo.scapy.          1800    IN      A       1.1.1.1
```

dig to *.loop from a dig-client
```text
# dig to a root server
$ docker exec dig-client dig @172.20.0.30 www.example.loop +norec +noall +answer +auth +add
loop.                   3600    IN      NS      ns03.loop.
loop.                   3600    IN      NS      ns07.loop.
loop.                   3600    IN      NS      ns05.loop.
loop.                   3600    IN      NS      ns06.loop.
loop.                   3600    IN      NS      ns02.loop.
loop.                   3600    IN      NS      ns08.loop.
loop.                   3600    IN      NS      ns01.loop.
loop.                   3600    IN      NS      ns04.loop.
ns08.loop.              3600    IN      A       172.20.0.71
ns07.loop.              3600    IN      A       172.20.0.70
ns06.loop.              3600    IN      A       172.20.0.69
ns05.loop.              3600    IN      A       172.20.0.68
ns04.loop.              3600    IN      A       172.20.0.67
ns03.loop.              3600    IN      A       172.20.0.66
ns02.loop.              3600    IN      A       172.20.0.65
ns01.loop.              3600    IN      A       172.20.0.64

# dig to loop server(faked auth servers)
# get a referral reponse
$ docker exec dig-client dig @172.20.0.71 www.example.loop +norec +noall +answer +auth +add
example.loop.           1800    IN      NS      ns01.txybmbkycl.loop.
example.loop.           1800    IN      NS      ns01.ldzuyaoivj.loop.
example.loop.           1800    IN      NS      ns01.ctdkceagsa.loop.
example.loop.           1800    IN      NS      ns01.sribmnwtiq.loop.
example.loop.           1800    IN      NS      ns01.cjkfnewuql.loop.
example.loop.           1800    IN      NS      ns01.ckpelxrfvq.loop.
example.loop.           1800    IN      NS      ns01.lvkxglhzrv.loop.
example.loop.           1800    IN      NS      ns01.jdhfmnttob.loop.
ns01.txybmbkycl.loop.   1800    IN      A       172.20.0.64
ns01.ldzuyaoivj.loop.   1800    IN      A       172.20.0.65
ns01.ctdkceagsa.loop.   1800    IN      A       172.20.0.66
ns01.sribmnwtiq.loop.   1800    IN      A       172.20.0.67
ns01.cjkfnewuql.loop.   1800    IN      A       172.20.0.68
ns01.ckpelxrfvq.loop.   1800    IN      A       172.20.0.69
ns01.lvkxglhzrv.loop.   1800    IN      A       172.20.0.70
ns01.jdhfmnttob.loop.   1800    IN      A       172.20.0.71
```

# 6. About Caching Name Servers

When starting containers with this compose file, all cache DNS containers are configured to refer to an internal root server as its hints.

# 7. About BIND Caching Name Server

When caching name sesrvers send queries to faked auth servers(scapy), faked auth servers will retrun ICMP port unrechable packets and faked DNS responses.
When BIND recieves an ICMP port unreachable packet before recieving a DNS response, BIND seems to regard its reply as servfail.
On the other hand, unbound seems to ignore an ICMP port unreachable packet and accept faked DNS reponses from scapy containers.

So I configure nftables to block ICMP port unrechable in BIND cache containers as a workaround.
This configuration exists in only BIND cache containers.

```text
$ cat Docker_build/bind_build_22.04/nftables.conf 
#!/usr/sbin/nft -f

flush ruleset

table inet filter {
        chain input {
                type filter hook input priority 0; policy accept;
                icmp type destination-unreachable counter drop
        }
        chain forward {
                type filter hook forward priority 0; policy accept;
        }
        chain output {
                type filter hook output priority 0; policy accept;
        }
}
```

# 8. Send `www.foobar.loop` to unbound from dig-client

```
$ docker exec unbound unbound-control flush all
ok

# send a query to unbound.
# servfail is expected result because faked auth servers return infinite delegation reponses.
$ docker exec dig-client dig @172.20.0.15 www.foobar.loop +retry=0 +timeout=300

; <<>> DiG 9.18.1-1ubuntu1.2-Ubuntu <<>> @172.20.0.15 www.foobar.loop +retry=0 +timeout=300
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: SERVFAIL, id: 59961
;; flags: qr rd ra; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;www.foobar.loop.               IN      A

;; Query time: 2139 msec
;; SERVER: 172.20.0.15#53(172.20.0.15) (UDP)
;; WHEN: Wed Sep 28 13:21:11 UTC 2022
;; MSG SIZE  rcvd: 44

# capture data ( dig-client : 172.20.0.3, unbound : 172.20.0.15 )
$ tshark -nn -r unbound.cap | head -20
1   0.000000   172.20.0.3 → 172.20.0.15  DNS 98 Standard query 0xea39 A www.foobar.loop OPT
2   0.000580  172.20.0.15 → 172.20.0.67  DNS 86 Standard query 0x6e44 A www.foobar.loop OPT
3   0.046771  172.20.0.67 → 172.20.0.15  DNS 734 Standard query response 0x6e44 A www.foobar.loop NS ns01.jzytwkfhzs.loop NS ns01.grkjfcekuo.loop NS ns01.etejhculxq.loop NS ns01.dskwuytwuc.loop NS ns01.zwzxklgnig.loop NS ns01.qwiawuqvme.loop NS ns01.rguxsjlwkr.loop NS ns01.ujbwyoxtuo.loop A 172.20.0.64 A 172.20.0.65 A 172.20.0.66 A 172.20.0.67 A 172.20.0.68 A 172.20.0.69 A 172.20.0.70 A 172.20.0.71 OPT
4   0.049788  172.20.0.15 → 172.20.0.65  DNS 86 Standard query 0x322a A www.foobar.loop OPT
5   0.114655  172.20.0.65 → 172.20.0.15  DNS 734 Standard query response 0x322a A www.foobar.loop NS ns01.stafnfbqxw.loop NS ns01.ojekawdybv.loop NS ns01.lvfkycpnec.loop NS ns01.sqdlgezonl.loop NS ns01.xbisdvdqte.loop NS ns01.kwoyzjzmga.loop NS ns01.jpvtpsbwia.loop NS ns01.zqkiktzkhw.loop A 172.20.0.64 A 172.20.0.65 A 172.20.0.66 A 172.20.0.67 A 172.20.0.68 A 172.20.0.69 A 172.20.0.70 A 172.20.0.71 OPT
6   0.117662  172.20.0.15 → 172.20.0.69  DNS 86 Standard query 0x9d02 A www.foobar.loop OPT
7   0.179379  172.20.0.69 → 172.20.0.15  DNS 734 Standard query response 0x9d02 A www.foobar.loop NS ns01.setjikocne.loop NS ns01.cxgjjrkvps.loop NS ns01.zhmungmosq.loop NS ns01.gtdxshjgkf.loop NS ns01.rplpaamlyt.loop NS ns01.etoqmyjjyh.loop NS ns01.jpylxsguvk.loop NS ns01.qryzsademu.loop A 172.20.0.64 A 172.20.0.65 A 172.20.0.66 A 172.20.0.67 A 172.20.0.68 A 172.20.0.69 A 172.20.0.70 A 172.20.0.71 OPT
8   0.182321  172.20.0.15 → 172.20.0.66  DNS 86 Standard query 0xe537 A www.foobar.loop OPT
9   0.250757  172.20.0.66 → 172.20.0.15  DNS 734 Standard query response 0xe537 A www.foobar.loop NS ns01.nmykbvctmt.loop NS ns01.kriyqvrrwn.loop NS ns01.ioidynfuex.loop NS ns01.ytyftlcoku.loop NS ns01.slssrydaxi.loop NS ns01.avdtlasbuv.loop NS ns01.dcjkajeeqv.loop NS ns01.bqoprkniyh.loop A 172.20.0.64 A 172.20.0.65 A 172.20.0.66 A 172.20.0.67 A 172.20.0.68 A 172.20.0.69 A 172.20.0.70 A 172.20.0.71 OPT
10   0.252049  172.20.0.15 → 172.20.0.68  DNS 86 Standard query 0x774d A www.foobar.loop OPT
11   0.321409  172.20.0.68 → 172.20.0.15  DNS 734 Standard query response 0x774d A www.foobar.loop NS ns01.izrhjispzk.loop NS ns01.wcnkjmqdec.loop NS ns01.qdvmnyzbpx.loop NS ns01.hdolyvlykp.loop NS ns01.hccpioqspv.loop NS ns01.avsbpbfwfm.loop NS ns01.aglbviodcj.loop NS ns01.tzpzrrmdai.loop A 172.20.0.64 A 172.20.0.65 A 172.20.0.66 A 172.20.0.67 A 172.20.0.68 A 172.20.0.69 A 172.20.0.70 A 172.20.0.71 OPT
12   0.323430  172.20.0.15 → 172.20.0.64  DNS 86 Standard query 0x6023 A www.foobar.loop OPT
13   0.390457  172.20.0.64 → 172.20.0.15  DNS 734 Standard query response 0x6023 A www.foobar.loop NS ns01.chgpcbillb.loop NS ns01.vyznalvdpp.loop NS ns01.tbawjmdewf.loop NS ns01.ygdpzpjppa.loop NS ns01.uldzktqlnn.loop NS ns01.sbhdrtkshn.loop NS ns01.rwljypcxky.loop NS ns01.bzmltymqpl.loop A 172.20.0.64 A 172.20.0.65 A 172.20.0.66 A 172.20.0.67 A 172.20.0.68 A 172.20.0.69 A 172.20.0.70 A 172.20.0.71 OPT
14   0.393437  172.20.0.15 → 172.20.0.68  DNS 86 Standard query 0xa859 A www.foobar.loop OPT
15   0.451852  172.20.0.68 → 172.20.0.15  DNS 734 Standard query response 0xa859 A www.foobar.loop NS ns01.nxvxehlzzh.loop NS ns01.lkcfrftxjj.loop NS ns01.sjpolhwmgw.loop NS ns01.bfcwxgvcmc.loop NS ns01.xvelfcjcpi.loop NS ns01.vzwhyufbdh.loop NS ns01.aolgjqtwoc.loop NS ns01.xjlbjnzygk.loop A 172.20.0.64 A 172.20.0.65 A 172.20.0.66 A 172.20.0.67 A 172.20.0.68 A 172.20.0.69 A 172.20.0.70 A 172.20.0.71 OPT
16   0.453602  172.20.0.15 → 172.20.0.66  DNS 86 Standard query 0x7b1d A www.foobar.loop OPT
17   0.501930  172.20.0.66 → 172.20.0.15  DNS 734 Standard query response 0x7b1d A www.foobar.loop NS ns01.eqhvodjkmf.loop NS ns01.znlfqruyij.loop NS ns01.dzrepbzdsx.loop NS ns01.vajxujblyn.loop NS ns01.yhzvatkuui.loop NS ns01.zjrnjgyqzs.loop NS ns01.tdmqzzwimx.loop NS ns01.cwowkmbteu.loop A 172.20.0.64 A 172.20.0.65 A 172.20.0.66 A 172.20.0.67 A 172.20.0.68 A 172.20.0.69 A 172.20.0.70 A 172.20.0.71 OPT
18   0.503868  172.20.0.15 → 172.20.0.71  DNS 86 Standard query 0x4937 A www.foobar.loop OPT
19   0.562272  172.20.0.71 → 172.20.0.15  DNS 734 Standard query response 0x4937 A www.foobar.loop NS ns01.kmbqbqsrfq.loop NS ns01.ansjmmlbdg.loop NS ns01.tzkomqjimx.loop NS ns01.nzycrzsdxt.loop NS ns01.fzdeimwbtf.loop NS ns01.klhnllreqp.loop NS ns01.nopgxjpxcm.loop NS ns01.lrtyylltvk.loop A 172.20.0.64 A 172.20.0.65 A 172.20.0.66 A 172.20.0.67 A 172.20.0.68 A 172.20.0.69 A 172.20.0.70 A 172.20.0.71 OPT
20   0.564923  172.20.0.15 → 172.20.0.70  DNS 86 Standard query 0x47f9 A www.foobar.loop OPT

$ docker logs unbound | grep 'exceeded' -A1
[1664371154] unbound[1:0] debug: request has exceeded the maximum number of sends with 33
[1664371154] unbound[1:0] debug: return error response SERVFAIL
```

# 9. About Docker host

This compose file will launch an init container, so please make sure you are using cgroup v1 instead of v2.
If you want to know more about this, please see.

- https://serverfault.com/questions/1053187/systemd-fails-to-run-in-a-docker-container-when-using-cgroupv2-cgroupns-priva
- https://github.com/systemd/systemd/issues/13477#issuecomment-528113009

```text
$ cat /proc/cmdline 
BOOT_IMAGE=/boot/vmlinuz-5.15.0-48-generic root=UUID=4db44fd6-e7c2-4c96-be7f-450a80786f12 ro quiet splash systemd.unified_cgroup_hierarchy=0 vt.handoff=7

$ docker info |grep -i cgroup
 Cgroup Driver: cgroupfs
 Cgroup Version: 1
```

```text
$ cat /etc/lsb-release |tail -1
DISTRIB_DESCRIPTION="Ubuntu 22.04.1 LTS"

$ docker info
Client:
 Context:    default
 Debug Mode: false
 Plugins:
  app: Docker App (Docker Inc., v0.9.1-beta3)
  buildx: Docker Buildx (Docker Inc., v0.9.1-docker)
  compose: Docker Compose (Docker Inc., v2.10.2)
  scan: Docker Scan (Docker Inc., v0.17.0)

Server:
 Containers: 5
  Running: 2
  Paused: 0
  Stopped: 3
 Images: 476
 Server Version: 20.10.18
 Storage Driver: overlay2
  Backing Filesystem: extfs
  Supports d_type: true
  Native Overlay Diff: true
  userxattr: false
 Logging Driver: json-file
 Cgroup Driver: cgroupfs
 Cgroup Version: 1
 Plugins:
  Volume: local
  Network: bridge host ipvlan macvlan null overlay
  Log: awslogs fluentd gcplogs gelf journald json-file local logentries splunk syslog
 Swarm: inactive
 Runtimes: io.containerd.runtime.v1.linux runc io.containerd.runc.v2
 Default Runtime: runc
 Init Binary: docker-init
 containerd version: 9cd3357b7fd7218e4aec3eae239db1f68a5a6ec6
 runc version: v1.1.4-0-g5fd4c4d
 init version: de40ad0
 Security Options:
  apparmor
  seccomp
   Profile: default
 Kernel Version: 5.15.0-48-generic
 Operating System: Ubuntu 22.04.1 LTS
 OSType: linux
 Architecture: x86_64
 CPUs: 12
 Total Memory: 62.71GiB
 Name: desktop
 ID: 2TPD:7WEL:XE55:DEWM:IO6N:RYMN:M7HK:3ETF:YXAV:2M24:VP7W:UYUQ
 Docker Root Dir: /var/lib/docker
 Debug Mode: false
 Registry: https://index.docker.io/v1/
 Labels:
 Experimental: false
 Insecure Registries:
  127.0.0.0/8
 Live Restore Enabled: false
```