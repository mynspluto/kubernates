kubectl create namespace hadoop
kubectl config set-context --current --namespace=hadoop

docker build -t hadoop:latest ./hadoop
kubectl apply -f ./hadoop/svc.yml --namespace=hadoop
kubectl apply -f ./hadoop/one.yml --namespace=hadoop

nohup kubectl port-forward service/hadoop-service 9870 -n hadoop > port-forward.log 2>&1
