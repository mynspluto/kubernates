kubectl create namespace kafka
kubectl config set-context --current --namespace=kafka

helm repo add confluentinc https://packages.confluent.io/helm
helm repo update
helm upgrade --install \
 confluent-operator confluentinc/confluent-for-kubernetes
kubectl get pods
kubectl apply -f ./kafka/platform-kraft.yml

kubectl wait --for=condition=Ready --timeout=300s pod/kraftcontroller-0
kubectl wait --for=condition=Ready --timeout=300s pod/connect-0
kubectl wait --for=condition=Ready --timeout=300s pod/controlcenter-0
kubectl wait --for=condition=Ready --timeout=300s pod/kafka-0
kubectl wait --for=condition=Ready --timeout=300s pod/kafkarestproxy-0
kubectl wait --for=condition=Ready --timeout=300s pod/ksqldb-0
kubectl wait --for=condition=Ready --timeout=300s pod/schemaregistry-0

nohup kubectl port-forward controlcenter-0 9021:9021 -n kafka > port-forward.log 2>&1
nohup kubectl port-forward svc/kafkarestproxy 8082:8082 -n kafka > port-forward.log 2>&1

# Get the cluster address
#CLUSTER_ADDRESS=$(curl -s -X GET "http://localhost:8082/v3/clusters" | jq -r '.[0].bootstrap_servers')
#echo $CLUSTER_ADDRESS
# Use the cluster address in the second command
#curl -X GET "$CLUSTER_ADDRESS/v3/clusters/28e637f6-5449-4e11-a5w/topics/test_1/configs"


