# 실행

cd ../all-in-one
./start-minikube.sh
cd ../kafka-native-k8s
kubectl apply -f dep.yml
kubectl apply -f svc.yml

# 테스트

cd /home/mynspluto/다운로드/kafka_2.13-3.9.0/bin
./kafka-console-producer.sh --broker-list localhost:9092 --topic test-topic
./kafka-topics.sh --bootstrap-server localhost:9092 --list
