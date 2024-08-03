minikube ssh
docker images
docker rmi 기존hadoop이미지id
docker build -t hadoop:latest .
minikube image load hadoop:latest

kubectl delete all --all -n hadoop (pv, pvc는 안지워짐)
kubectl delete pvc --all -n hadoop
kubectl delete pv hadoop-pv

kubectl apply -f one.yml
kubectl delete -f one.yml

kubectl port-forward service/hadoop-namenode-service 9870(port: 1234면 1234, 9870이라 9870인거임)

sd 접속
