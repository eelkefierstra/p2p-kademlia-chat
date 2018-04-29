#!/bin/sh

openssl req -newkey rsa:2048 -new -x509 -days 365 -nodes -out ./mongodb-cert.crt -keyout ./mongodb-cert.key -subj '/CN=localhost'

cat ./mongodb-cert.key ./mongodb-cert.crt > ./mongodb.pem

mkdir -p /etc/ssl
cp ./mongodb-cert.crt ./mongodb.pem /etc/ssl/

