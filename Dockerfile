FROM python:3.7.3-alpine3.9
ENV OJ_ENV development

ADD . /app
WORKDIR /app

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk add  mariadb-dev
RUN apk add --update build-base nginx openssl curl unzip supervisor jpeg-dev zlib-dev freetype-dev
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r /app/requirements.txt
RUN apk del build-base --purge


ENTRYPOINT /app/deploy/entrypoint.sh
