FROM docker.io/debian:bookworm as openssl
LABEL maintainer="Matthew Vance"

ENV VERSION_OPENSSL=openssl-3.0.5 \
    SHA256_OPENSSL=aa7d8d9bef71ad6525c55ba11e5f4397889ce49c2c9349dcea6d3e4f0b024a7a \
    SOURCE_OPENSSL=https://www.openssl.org/source/ \
    OPGP_OPENSSL=7953AC1FBC3DC8B3B292393ED5E9E43F7DF9EE8C

WORKDIR /tmp/src

RUN set -e -x && \
    build_deps="build-essential ca-certificates curl dirmngr gnupg libidn2-0-dev libssl-dev" && \
    DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y --no-install-recommends \
      $build_deps && \
    curl -L $SOURCE_OPENSSL$VERSION_OPENSSL.tar.gz -o openssl.tar.gz && \
    echo "${SHA256_OPENSSL} ./openssl.tar.gz" | sha256sum -c - && \
    curl -L $SOURCE_OPENSSL$VERSION_OPENSSL.tar.gz.asc -o openssl.tar.gz.asc && \
    GNUPGHOME="$(mktemp -d)" && \
    export GNUPGHOME && \
    gpg --no-tty --keyserver keyserver.ubuntu.com --recv-keys "$OPGP_OPENSSL" && \
    gpg --batch --verify openssl.tar.gz.asc openssl.tar.gz && \
    tar xzf openssl.tar.gz && \
    cd $VERSION_OPENSSL && \
    ./config \
      --prefix=/opt/openssl \
      --openssldir=/opt/openssl \
      no-weak-ssl-ciphers \
      no-ssl3 \
      no-shared \
      enable-ec_nistp_64_gcc_128 \
      -DOPENSSL_NO_HEARTBEATS \
      -fstack-protector-strong && \
    make depend && \
    make && \
    make install_sw && \
    apt-get purge -y --auto-remove \
      $build_deps && \
    rm -rf \
        /tmp/* \
        /var/tmp/* \
        /var/lib/apt/lists/*

FROM docker.io/debian:bookworm as unbound
LABEL maintainer="Matthew Vance"

ENV NAME=unbound \
    UNBOUND_VERSION=1.20.0 \
    #UNBOUND_SHA256=2e32f283820c24c51ca1dd8afecfdb747c7385a137abe865c99db4b257403581 \
    UNBOUND_DOWNLOAD_URL=https://nlnetlabs.nl/downloads/unbound/unbound-1.20.0.tar.gz

WORKDIR /tmp/src

COPY --from=openssl /opt/openssl /opt/openssl

RUN build_deps="curl gcc libc-dev libevent-dev libexpat1-dev libnghttp2-dev make" && \
    set -x && \
    DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y --no-install-recommends \
      $build_deps \
      bsdmainutils \
      ca-certificates \
      ldnsutils \
      libevent-2.1-7 \
      libexpat1 \
      libprotobuf-c-dev \
      protobuf-c-compiler && \
    curl -sSL $UNBOUND_DOWNLOAD_URL -o unbound.tar.gz && \
    #echo "${UNBOUND_SHA256} *unbound.tar.gz" | sha256sum -c - && \
    tar xzf unbound.tar.gz && \
    rm -f unbound.tar.gz && \
    cd unbound-* && \
    groupadd _unbound && \
    useradd -g _unbound -s /dev/null -d /etc _unbound && \
    ./configure \
        --disable-dependency-tracking \
        --prefix=/opt/unbound \
        --with-pthreads \
        --with-username=_unbound \
        --with-ssl=/opt/openssl \
        --with-libevent \
        --with-libnghttp2 \
        --enable-dnstap \
        --enable-tfo-server \
        --enable-tfo-client \
        --enable-event-api \
        --enable-subnet && \
    make install && \
    mv /opt/unbound/etc/unbound/unbound.conf /opt/unbound/etc/unbound/unbound.conf.example && \
    apt-get purge -y --auto-remove \
      $build_deps && \
    rm -rf \
        /opt/unbound/share/man \
        /tmp/* \
        /var/tmp/* \
        /var/lib/apt/lists/*


FROM docker.io/debian:bookworm
LABEL maintainer="Matthew Vance"

ENV NAME=unbound \
    VERSION=1.0 \
    SUMMARY="${NAME} is a validating, recursive, and caching DNS resolver." \
    DESCRIPTION="${NAME} is a validating, recursive, and caching DNS resolver."

WORKDIR /tmp/src

COPY --from=unbound /opt /opt

RUN set -x && \
    DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y --no-install-recommends \
      bsdmainutils \
      ca-certificates \
      ldnsutils \
      libevent-2.1-7 \
      libnghttp2-14 \
      libexpat1 \
      libprotobuf-c1 && \
    groupadd _unbound && \
    useradd -g _unbound -s /dev/null -d /etc _unbound && \
    apt-get purge -y --auto-remove \
      $build_deps && \
    rm -rf \
        /opt/unbound/share/man \
        /tmp/* \
        /var/tmp/* \
        /var/lib/apt/lists/*

COPY data/ /

RUN chmod +x /unbound.sh

WORKDIR /opt/unbound/

ENV PATH /opt/unbound/sbin:"$PATH"

LABEL org.opencontainers.image.version=${UNBOUND_VERSION} \
      org.opencontainers.image.title="mvance/unbound" \
      org.opencontainers.image.description="a validating, recursive, and caching DNS resolver" \
      org.opencontainers.image.url="https://github.com/MatthewVance/unbound-docker" \
      org.opencontainers.image.vendor="Matthew Vance" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.source="https://github.com/MatthewVance/unbound-docker"

WORKDIR /
RUN apt-get update && apt-get install -y nftables && rm -f /etc/nftables.conf
ADD ./nftables.conf /etc/nftables.conf

EXPOSE 53/tcp
EXPOSE 53/udp
EXPOSE 8953/udp

WORKDIR /opt/unbound/

HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 CMD drill @127.0.0.1 cloudflare.com || exit 1

CMD ["/unbound.sh"]
