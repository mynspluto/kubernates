minikube delete
minikube start --memory 15976

helm repo add confluentinc https://packages.confluent.io/helm
helm repo update
helm upgrade --install \
 confluent-operator confluentinc/confluent-for-kubernetes
kubectl get pods

kubectl apply -f 1.yml
kubectl apply -f 2.yml

kubectl port-forward controlcenter-0 9021:9021
127.0.0.1:9021 접속(컨트롤센터 웹)

image pull error 뜨는 경우
docker pull confluentinc/cp-kafka-rest:7.6.1.arm64 이런식으로 수동으로 받은후
minikube image load confluentinc/cp-kafka-rest:7.6.1.arm64 하여 이미지 로드

crashback error 뜨는 경우
minikube delete
minikube start --memory 15976 (15976은 도커 데스크탑앱 설정에서 제한되는듯)

replica 1로 바꾸면 에러남
metadata.namespace바꿔도 에러나는듯

todo
airflow로 하루에 한번 주가 데이터 수집
수집한 데이터 하둡으로 저장
저장했다고 카프카 메시지로 알림
쿠버네티스에 deployment로 등록된 카프카 소비자가 이를 감지
하둡으로 저장했던 파일을 스파크를 통해 로드
전처리를 하여 보조지표 등 필요한 데이터 파싱
학습
학습된 모델 하둡으로 저장
