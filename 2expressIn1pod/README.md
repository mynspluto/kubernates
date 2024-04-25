application에서 docker 실행
kubectl config use-context minikube
minikube start

cd express
docker build -t express:latest .
minikube image load express:latest

cd express2
docker build -t express:latest .
minikube image load express:latest

kubectl apply -f express-deployment.yml

- 여기서 파드 생성됨, 컨테이너 포트의 역할 모르겠음

kubectl apply -f express-service.yml
kubectl port-forward service/nodejs-app 31000
127.0.0.1:31000으로 접속

express-service.yml의 targetPort이랑 express/bin/www의 포트랑 연결됨
targetPort를 3001로하면 express로 3002로하면 express2로 연결됨
