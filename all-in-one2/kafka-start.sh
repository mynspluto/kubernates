kubectl create namespace kafka
kubectl config set-context --current --namespace=kafka

kubectl apply -f ./kafka/dep.yml
#kubectl wait --for=condition=ready --timeout=120s pod/kafka-0
#kubectl wait --for=condition=ContainersReady statefulset/kafka --timeout=60s
#kubectl wait --for='jsonpath={.status.conditions[?(@.type=="ContainersReady")]}' --timeout=120s pod/kafka-0 # kubectl get pod kafka-0 -o json
kubectl wait --for=jsonpath='{.status.phase}'=Running --timeout=120s pod/kafka-0 # kubectl get pod kafka-0 -o json
# TODO 특정 로그(카프카 실행완료)가 쌓이는걸 확인하고 실행

kubectl exec -it kafka-0 -- /opt/kafka/bin/kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092

#deploy 생성전에 svc 생성되는 경우 
#log4j:ERROR Could not read configuration file from URL [file:/opt/kafka/config/tools-log4j.properties]. 
#java.io.FileNotFoundException: /opt/kafka/config/tools-log4j.properties
kubectl apply -f ./kafka/svc.yml
#kubectl wait --for=condition=Ready --timeout=120s svc/kafka-service
nohup kubectl port-forward svc/kafka-service 9092:9092 -n kafka > port-forward.log 2>&1 &