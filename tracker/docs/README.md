# Installing the tracker
Run `setup.py install` for installing the tracker

# install mongodb-server
```
sudo apt install mongodb-server
```

# Configuring the tracker
```
cd /etc/ssl
```

Generate certificate, set the FQDN to localhost:
```
openssl req -newkey rsa:2048 -new -x509 -days 365 -nodes -out mongodb-cert.crt -keyout mongodb-cert.key
```

Generate pem file:
```
cat mongodb-cert.key mongodb-cert.crt > mongodb.pem
```

Edit /etc/mongodb.conf:

```
# SSL options
# Enable SSL on normal ports
sslOnNormalPorts = true
# SSL Key file and password
sslPEMKeyFile = /etc/ssl/mongodb.pem
#sslPEMKeyPassword = pass
```

## Testing mongodb
Start the mongodb service
```
systemctl start mongodb.service
```

In order to get the mongo shell, type the following command:
```
mongo --host localhost --ssl --sslPEMKeyFile /etc/ssl/mongodb.pem  --sslCAFile /etc/ssl/mongodb-cert.crt
```

If you get a shell, your connection is encrypted and ready for p2p-chat!
