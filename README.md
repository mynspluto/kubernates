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

윈도우 powershell에서 ubuntu 접속시
=> kubectl get nodes시 에러 cannot find ~~
=> sudo swapoff -a가 일시적으로 적용되어서 생기는 에러
=> sudo swapoff -a 후 몇 초 지나면 다시 정상 작동함

service로 pod간 continer간 연결이 안되는 경우 coredns가 kube-system에 있는지 확인
=> kubectl get pod -n kube-system
없는 경우 minikube stop, minikube delete, minikube start로 coredns가 생기게 유도
