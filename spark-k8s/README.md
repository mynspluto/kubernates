kubectl apply -f spark-master-deployment.yml
kubectl apply -f spark-master-svc.yml

kubectl port-forward service/spark-master 8080

127.0.0.1:8080 접속

시간이 흐른뒤 minikube가 꺼진후 minikube start를 하면 pod가 에러상태가 됨
이때 deployment만 지웠다가 생성하면 에러 발생
svc가 지워져있는 상태에서 deployment를 재생성해야 정상적으로 running 상태로 변경됨
