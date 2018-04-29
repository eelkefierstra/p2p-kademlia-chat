FROM mongo

#RUN apk add mongodb openssl --no-cache

WORKDIR /install
ADD . /install

RUN ls -la
RUN ./gen-cert.sh

CMD ["mongod", "--sslMode", "requireSSL", "--sslPEMKeyFile", "/etc/ssl/mongodb.pem", "--sslCAFile", "/etc/ssl/mongodb-cert.crt"]
