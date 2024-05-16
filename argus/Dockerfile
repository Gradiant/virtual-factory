FROM ubuntu:20.04

RUN apt-get update -qq && \
    apt-get install -yq netcat gcc make bison flex libpcap-dev libwrap0-dev argus-client argus-server inetutils-ping --no-install-recommends

COPY /config/argus.conf /etc/argus.conf
COPY /config/ra.conf /etc/ra.conf
COPY /config/argus_logrotate /etc/logrotate.d/argus.out
RUN chmod 644 /etc/logrotate.d/argus.out
RUN chown root:root /etc/logrotate.d/argus.out

EXPOSE 32000