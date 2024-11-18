kubectl create namespace hadoop
kubectl config set-context --current --namespace=hadoop

kubectl apply -f ./hadoop/config.yml --namespace=hadoop
kubectl apply -f ./hadoop/all.yml --namespace=hadoop

nohup kubectl port-forward service/namenode 9870 -n hadoop > port-forward.log 2>&1