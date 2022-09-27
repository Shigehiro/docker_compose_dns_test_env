# Docker Compose DNS test environment setup

# Description

- set up caching name servers, such as BIND, unbound
- set up authoritative name servers with BIND
  - one internal root server, two .com, two example.com
- set up broken auth name servers with python scapy

# How to run docker-compose

```text
docker-compose build --no-build bind-cache-old
docker-compose --no-cache bind-cache-old
docker-compose up -d
```

# About DNS Domains configured by this compose file

- *.example.com domain
  - BIND auth servers return answers for this domain
- *.scapy domain
  - scapy faked auth servers return queries for *.scpay domain, such as a.foo.capy, b.bar.scapy, c.foobar.scapy, whatever queries ended with *.scapy
- *.loop domain
  - scapy faked auth servers return inifnit loop delegations
  - whatever queries ended with *.loop

# Dig output

dig to *.example.com from a dig-client
```
```

dig to *.scapy from a dig-client
```
```

dig to *.loop from a dig-client
```
```

# About Caching Name Servers

When starting containers with this compose file, all cache DNS containers are configured to refer to an internal root server as its hints.

# About BIND Caching Name Server

When BIND cache sesrvers send queries to faked auth servers(scapy), faked auth servers will retrun ICMP port unrechable packets and faked DNS responses.
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

# About Docker host

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