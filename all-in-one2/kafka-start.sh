kubectl create namespace kafka
kubectl config set-context --current --namespace=kafka

kubectl apply -f ./kafka/dep.yml
kubectl wait --for=condition=available --timeout=120s deployment/kafka 
#deploy 생성전에 svc 생성되는 경우 
#log4j:ERROR Could not read configuration file from URL [file:/opt/kafka/config/tools-log4j.properties]. 
#java.io.FileNotFoundException: /opt/kafka/config/tools-log4j.properties
kubectl apply -f ./kafka/svc.yml
#kubectl wait --for=condition=Ready --timeout=120s svc/kafka-service
nohup kubectl port-forward svc/kafka-service 9092:9092 -n kafka > port-forward.log 2>&1 &