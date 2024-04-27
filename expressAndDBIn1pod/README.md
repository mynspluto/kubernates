cd exress
docker build -t express_db:latest .
minikube image load express_db:latest

kubectl apply -f deployment.yml
kubectl apply -f service.yml
kubectl port-forward service/express-db-service 31000
