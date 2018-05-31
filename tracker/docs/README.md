# Setting up the tracker

## Firewall configuration
To prevent the server from being hacked during the configuration, please
perform the following steps:

1. Set the firewall policy to block all ports, except ssh if needed. Make sure
   you don't lock out yourself!
2. Open the following ports:
    * 1337 (TCP server)
    * 8468 (P2P bootstrap server)

## Setting up a MongoDB server
### Installation
```
sudo apt-get -y install mongodb-server
```

### Configuration
```
cd /etc/ssl
```

Generate certificate, set the FQDN to localhost:
```
sudo openssl req -newkey rsa:2048 -new -x509 -days 365 -nodes -out mongodb-cert.crt -keyout mongodb-cert.key
```

Generate pem file:
```
cat mongodb-cert.key mongodb-cert.crt | sudo tee mongodb.pem
```

Edit /etc/mongodb.conf:

```
sudoedit /etc/mongodb.conf

Change the following:
# SSL options
# Enable SSL on normal ports
sslOnNormalPorts = true
# SSL Key file and password
sslPEMKeyFile = /etc/ssl/mongodb.pem
#sslPEMKeyPassword = pass
```

### Testing the MongoDB database
Start the mongodb service
```
systemctl start mongodb.service
```

In order to get the mongo shell, run the following command:
```
mongo --host localhost --ssl --sslPEMKeyFile /etc/ssl/mongodb.pem  --sslCAFile /etc/ssl/mongodb-cert.crt
```

If you get a shell, your connection is encrypted and ready for p2p-chat!

## Installation of the tracker
Run `setup.py install` for installing the tracker

## Testing the tracker
To start the tracker, run the following command:
```
src/main.py ./mongodb-cert.key ./mongodb-cert.crt --iface 0.0.0.0
```

Test your tracker by doing the following:
1. Start a client with `src/main.py --host <tracker ip address>`
2. Create a chat
3. Send a message in this chat
4. Start another chat client, the same way as you started step 1.
5. Join the chat with the chatuuid shown in step 2.
6. Check whether the second client received the chat message sent in step 3.
7. Send a message with the second client and check whether the first client
   received it.

## Running the tracker
Run the tracker by setting up a watchdog for it, run it as a service, or on
a terminal multiplexer over ssh to prevent the program from being closed after
closing the SSH session.


