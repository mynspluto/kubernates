minikube ssh
docker images
docker rmi 기존hadoop이미지id
docker build -t hadoop:latest .
minikube image load hadoop:latest

kubectl delete configmap hadoop-config
kubectl delete -f namenode-deployment.yml
kubectl apply -f config.yml
kubectl apply -f namenode-deployment.yml

kubectl apply -f namenode-svc.yml
kubectl port-forward service/hadoop-namenode-service 9870(port: 1234면 1234, 9870이라 9870인거임)

sd 접속
