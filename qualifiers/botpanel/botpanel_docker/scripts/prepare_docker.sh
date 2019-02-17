#! /bin/bash

function check_root {
  if [[ $EUID -ne 0 ]]; then
   echo "[-] This script must be run as root" 1>&2
   exit 1
  fi
}

echo "CTFFramework Builder v1"
check_root

echo "[+] Updating and upgrading ..."
apt-get -y update --fix-missing
apt-get -y upgrade

echo "[+] Generating locale ..."
locale-gen en_US.UTF-8
locale-gen sv_SE.UTF-8

echo "[+] Installing deps ..."
apt-get -y install $(cat dependencies.txt)

echo "[+] Installing docker ..."
apt-get -y remove docker docker-engine
apt-get -y install \
    linux-image-extra-$(uname -r) \
    linux-image-extra-virtual
apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
 add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
apt-get -y update --fix-missing
apt-get -y install docker-ce

echo "[+] Installing docker-compose"
curl -L https://github.com/docker/compose/releases/download/1.20.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

usermod -aG docker ubuntu

echo "[+] Running Docker test ..."
docker-compose --version

echo "docker start \$(docker ps -q -a)" > start_challs.sh
chmod +x start_challs.sh
echo "docker stop \$(docker ps -q)" > stop_challs.sh
chmod +x stop_challs.sh
