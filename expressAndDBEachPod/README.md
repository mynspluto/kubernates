cd exress
docker build -t express_db_each_pod:latest .
minikube image load express_db_each_pod

kubectl apply -f deployment-express.yml
kubectl apply -f deployment-maria.yml
kubectl apply -f service-express.yml
kubectl apply -f service-maria.yml

kubectl port-forward service/express-service 31000
(minikube service express-service --url 이것도 가능)
