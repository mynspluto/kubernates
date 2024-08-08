minikube ssh
docker images
docker rmi 기존hadoop이미지id
docker build -t hadoop:latest .
minikube image load hadoop:latest

kubectl create namespace hadoop
kubectl config set-context --current --namespace=hadoop

kubectl delete all --all -n hadoop (pv, pvc는 안지워짐)
kubectl delete pvc --all -n hadoop
kubectl delete pv hadoop-pv

kubectl apply -f one.yml --namespace=hadoop
kubectl apply -f svc.yml --namespace=hadoop

kubectl delete -f one.yml --namespace=hadoop
kubectl delete -f svc.yml --namespace=hadoop

kubectl get endpoints -n hadoop

kubectl port-forward service/hadoop-service 9870(port: 1234면 1234, 9870이라 9870인거임)
