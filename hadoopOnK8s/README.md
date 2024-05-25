minikube ssh
docker images
docker rmi 기존hadoop이미지id
docker build -t hadoop:latest .
minikube image load hadoop:latest

kubectl delete configmap hadoop-config
kubectl delete -f namenode-deployment.yml
kubectl apply -f config.yml
kubectl apply -f namenode-deployment.yml
