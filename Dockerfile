FROM certbot/certbot:latest

#http://dl-cdn.alpinelinux.org/alpine/
ENV TZ="Europe/Bratislava"

RUN \
 apk add --no-cache tzdata \
    && ln -sf /usr/share/zoneinfo/${TZ} /etc/localtime \
    && echo "${TZ}" > /etc/timezone && \
 apk add  --update curl && \
 rm -rf /var/cache/apk/* && \
 pip3 install requests
