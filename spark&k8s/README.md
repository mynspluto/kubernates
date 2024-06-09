kubectl apply -f spark-master-deployment.yml
kubectl apply -f spark-master-svc.yml

kubectl port-forward service/spark-master 8080

127.0.0.1:8080 접속
