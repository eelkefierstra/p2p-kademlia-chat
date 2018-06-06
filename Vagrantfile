Vagrant.configure("2") do |config|

    config.vm.define "tracker" do |tracker|
        tracker.vm.box = "ubuntu/xenial64"
        tracker.vm.hostname = "tracker"
        tracker.vm.network :private_network, ip: "192.168.56.101"
        tracker.vm.provider "virtualbox" do |v|
            v.gui = true
            v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
            v.customize ["modifyvm", :id, "--memory", 1024]
            v.customize ["modifyvm", :id, "--name", "p2pchat_tracker"]
        end
        tracker.vm.provision "shell", inline: "sudo apt-get update"
        tracker.vm.provision "shell", inline: "sudo apt-get install -y virtualbox-guest-dkms virtualbox-guest-utils python python3 mongodb-server rsync tmux python-pip python3-pip"
        tracker.vm.provision "shell", inline: "sudo systemctl enable mongodb"
        tracker.vm.provision "shell", inline: "pip install pipenv"

        $gencert = <<SCRIPT
        #!/bin/bash
        sudo openssl req -newkey rsa:2048 -new -x509 -days 365 -nodes -out /etc/ssl/mongodb-cert.crt -keyout /etc/ssl/mongodb-cert.key -subj "/CN=localhost"
        cat /etc/ssl/mongodb-cert.key /etc/ssl/mongodb-cert.crt | sudo tee /etc/ssl/mongodb.pem
SCRIPT

        tracker.vm.provision :shell, :inline => $gencert
        
        # Permit anyone to start the GUI
        #config.vm.synced_folder "tracker/", "/srv/tracker"
    end

    config.vm.define "client1" do |client1|
        client1.vm.box = "ubuntu/xenial64"
        client1.vm.hostname = "client"
        client1.vm.network :private_network, ip: "192.168.56.102"
        client1.vm.provider "virtualbox" do |v|
            v.gui = true
            v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
            v.customize ["modifyvm", :id, "--memory", 1024]
            v.customize ["modifyvm", :id, "--name", "p2pchat_client1"]
        end
        # Install xfce and virtualbox additions
        client1.vm.provision "shell", inline: "sudo apt-get update"
        client1.vm.provision "shell", inline: "sudo apt-get install -y xfce4 virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11 python python3 rsync python-pip python3-pip python3-tk"
        client1.vm.provision "shell", inline: "pip install pipenv"
        # Permit anyone to start the GUI
    end

    config.vm.define "client2" do |client2|
        client2.vm.box = "ubuntu/xenial64"
        client2.vm.hostname = "client"
        client2.vm.network :private_network, ip: "192.168.56.103"
        client2.vm.provider "virtualbox" do |v|
            v.gui = true
            v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
            v.customize ["modifyvm", :id, "--memory", 1024]
            v.customize ["modifyvm", :id, "--name", "p2pchat_client2"]
        end
        # Install xfce and virtualbox additions
        client2.vm.provision "shell", inline: "sudo apt-get update"
        client2.vm.provision "shell", inline: "sudo apt-get install -y xfce4 virtualbox-guest-dkms virtualbox-guest-utils virtualbox-guest-x11 python python3 rsync python-pip python3-pip python3-tk"
        client2.vm.provision "shell", inline: "pip install pipenv"
        # Permit anyone to start the GUI
    end
  
    #config.vm.synced_folder ".", "/vagrant", type: "rsync",
        #rsync__exclude: "*.db"
end
