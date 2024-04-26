todo
kubectl port-forward service/express-service 31000 이후 127.0.0.1/select 접속시
kubectl logs express-maria-deployment-64c9b78df-ss5kw -c express-container로 에러 확인하면
err : Error: ER_BAD_DB_ERROR: Unknown database 'kubernetes_express'
해당 디비를 생성하면서 테이블 생성, 데이터 삽입 시 정상 작동될 것으로 보임

cd exress
docker build -t express_db:latest .
minikube image load express_db:latest

kubectl apply -f deployment.yml
kubectl apply -f service.yml
kubectl port-forward service/express-db-service 31000
