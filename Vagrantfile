MACHINES = {
  "az-1" => "10.10.10.150",
  "az-2" => "10.10.10.151",
  "az-3" => "10.10.10.152",
}

$script = <<-SHELL
apt-get update
apt-get install -y python3 python3-apt
sudo apt-get remove -y --ignore-missing $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1) 2>/dev/null

# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install -y ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
sudo tee /etc/apt/sources.list.d/docker.sources <<-EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF

sudo apt-get update

sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Expose docker API
mkdir -p /etc/systemd/system/docker.service.d/
sudo tee /etc/systemd/system/docker.service.d/override.conf <<-EOF
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd -H fd:// -H tcp://0.0.0.0:2375 --containerd=/run/containerd/containerd.sock
EOF

sudo systemctl daemon-reload

sudo systemctl restart docker.service

usermod -aG docker vagrant
echo "TERM=xterm-256color" >> /etc/environment
SHELL

Vagrant.configure("2") do |config|
  config.vm.box = "cloud-image/ubuntu-24.04"
  config.vm.synced_folder ".", "/vagrant", type: "rsync"

  config.vm.provider :libvirt do |libvirt|
    libvirt.driver = "kvm"
    libvirt.memory = 2048
    libvirt.cpus = 2
    libvirt.graphics_type = "vnc"
    libvirt.video_type = "virtio"
    libvirt.management_network_keep = false
  end

  config.vm.provision "shell", inline: $script

  MACHINES.each do |hostname, ip_address|
    config.vm.define hostname do |node|
      node.vm.hostname = hostname

      node.vm.network "private_network",
        ip: ip_address
    end
  end
end
