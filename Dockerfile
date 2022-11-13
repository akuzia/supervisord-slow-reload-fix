FROM debian:bullseye

RUN apt-get update && \
    apt-get install -y supervisor python3

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
