kubectl get nodes => cannot cunnect ~
  systemctl restart docker

sudo kubeadm reset
sudo kubeadm start => 10248 healthz ~
  sudo vi /etc/docker/daemon.json
  {
    "exec-opts": ["native.cgroupdriver=systemd"], //croupdriver를 systemd로 설정
    "log-driver": "json-file",
    "log-opts": {
      "max-size": "100m"
    },
    "storage-driver": "overlay2"
  }
  sudo swapoff -a
