kubectl create namespace hadoop
kubectl config set-context --current --namespace=hadoop

sudo rm -rf /data/hadoop-config
sudo mkdir -p /data/hadoop-config
sudo chmod 777 /data/hadoop-config
sudo mkdir -p /data/hadoop-data
sudo chmod 777 /data/hadoop-data
cp -r ./hadoop/config/* /data/hadoop-config
nohup minikube mount /data/hadoop-config:/data/hadoop-config > mount.log 2>&1 &
nohup minikube mount /data/hadoop-data:/data/hadoop-data > mount.log 2>&1 &

kubectl apply -f ./hadoop/config.yml --namespace=hadoop
kubectl apply -f ./hadoop/all.yml --namespace=hadoop
kubectl wait --for=condition=available --timeout=120s deployment/namenode 

nohup kubectl port-forward service/namenode 9870 -n hadoop > port-forward.log 2>&1 &
