cd exress
docker build -t express_db_each_pod:latest . --no-cache
minikube image load express_db_each_pod:latest

kubectl get deployment
kubectl delete deployment express-deployment
kubectl delete deployment maria-deployment
kubectl delete pvc mysql-pv-claim
kubectl delete pv mysql-pv

kubectl apply -f pv-maria.yml
kubectl apply -f pvc-maria.yml

kubectl apply -f deployment-maria.yml
kubectl apply -f service-maria.yml

kubectl apply -f deployment-express.yml
kubectl apply -f service-express.yml

kubectl port-forward service/express-service 31000
(minikube service express-service --url 이것도 가능)

minikube addons list | grep ingress
minikube addons enable ingress
minikube addons enable ingress-dns

kubectl delete -A ValidatingWebhookConfiguration ingress-nginx-admission
=> 에러시 유효성 검증 제거
kubectl apply -f ingress-express.yml

sudo vi /etc/hosts
=> 127.0.0.1 example.com
minikube tunnel
example.com 접속

service로 pod간 continer간 연결이 안되는 경우 coredns가 kube-system에 있는지 확인
=> kubectl get pod -n kube-system
없는 경우 minikube stop, minikube delete, minikube start로 coredns가 생기게 유도

todo
mysql을 dockerFile로 만들게함
mysqld --initialize --datadir=/var/lib/mysql 해당명령어를 통해
File ./ibdata1: 'open' returned OS error 71. Cannot continue operation 이 에러가 안뜨게함
그러려면 sh를 작성하여 mysqld --initialize --datadir=/var/lib/mysql를 실행한뒤
CMD [mysql.start]를 해야할듯
