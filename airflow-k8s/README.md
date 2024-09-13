# 네임스페이스 생성 및 변경

kubectl create namespace airflow
kubectl config set-context --current --namespace=airflow

# 기존 요소 제거

helm uninstall airflow -n airflow
kubectl delete all --all -n airflow
docker system prune -a
minikube ssh
docker rmi mynspluto-airflow

# 이미지 생성, 이미지 로드

docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}"
docker build -t mynspluto-airflow:latest .

# 실행, 테스트

helm install airflow apache-airflow/airflow -n airflow -f values.yml
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow

id: admin
pw: admin

# dag 디버깅

kubectl exec -it airflow-worker-0 -- /bin/bash
cd logs

# 요소 업데이트

helm upgrade airflow apache-airflow/airflow -n airflow -f values.yml

# 컨테이너 bash 접속

kubectl get pod
kubectl exec -it airflow-webserver-948b685fd-5vhbd -- /bin/bash

# 카프카 토픽 미생성시 에러

- 클러스터 id 확인
  curl -X GET "http://localhost:8082/v3/clusters"

- test_1 topic 생성
  curl -X GET "http://localhost:8082/v3/clusters/28e637f6-5449-4e11-a5w/topics/test_1/configs"

dag 추가가 안되는 이슈
kubectl exec -it airflow-scheduler-69c669d4f-tt4p5 -- /bin/bash
ls /opt/airflow/dags/
=> 아무것도 안나옴
kubectl describe pod scheduler
=> 만든이미지가 적용 되는게 아니라 dockerhub?의 airflow:2.9.2를 가져다 쓰고 있음
values.yml을 https://airflow.apache.org/docs/helm-chart/stable/parameters-ref.html를 보고 키 값 맞춰서 제대로 작성해야될거 같음
https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/kubernetes_executor.html도 참고

주가 수집하는 dag 작성
하둡서버 돌리기, 카프카 서버 돌리기
pyspark등으로 하둡에저장, 저장후 카프카 메시지로 저장됐다고 알림
하둡 bash로 접근하여 저장됐는지 확인
카프카 소비자에서 저장됐단 메시지를 받고 하둡에 접근하여 파일 읽어온후 스파크에 올림
데이터 전처리
학습

# 리소스 사용량

NAME CPU(cores) MEMORY(bytes)  
airflow-postgresql-0 37m 83Mi  
airflow-redis-0 2m 9Mi  
airflow-scheduler-56f59c9dcd-4j6mv 825m 317Mi  
airflow-statsd-b45f54fb4-jxk5b 3m 9Mi  
airflow-triggerer-0 569m 481Mi  
airflow-webserver-7fbbd9ff5d-qh278 769m 835Mi  
airflow-worker-0 713m 1825Mi

# 하둡 + 에어플로우 리소스 사용량

NAME CPU(cores) CPU% MEMORY(bytes) MEMORY%  
minikube 3113m 38% 4863Mi 20%

# 하둡 kerberos auth

kerberos 사용시
kerberos 서버를 띄워야 함
kerberos 서버에서 kadmin ~~ 로 사용자 생성하면 키탭 파일이 생성됨
이 파일을 하둡서버와 하둡클라이언트(airflow 측) 으로 가져오고
하둡서버에서 키탭파일 경로를 지정(core-site ? hdfs-site)
하둡클라이언트에서 kinit -kt /path/to/client.keytab user@EXAMPLE.COM 키탭파일 지정하여 티켓 발급

krb5.conf
[domain_realm]
.example.com = hadoop-server.example.com
example.com = hadoop-server.example.com

webhdfs로 hadoop-server.example.com에 요청시 header authrization에 티켓포함

# kerberos 인증 로직

커버로스 서버, 하둡 서버, 클라이언트(에어플로우)가 있다고 가정
커버로스 서버에서 하둡을 위한 user를 생성하고 이 user에 대한 키탭파일을 생성
이 키탭 파일을 하둡 서버와 클라이언트에 저장
클라이언트에서 하둡에 뭔가 요청을 할 때
클라이언트는 키탭파일을 커버로스 서버에 전송하여 티켓(tgt Ticket-Granting Ticket)을 발급 받음
이 티켓(tgt)을 하둡 서버에 전송하여 하둡 서비스티켓을 발급 받음
하둡 서버에서는 본인이 저장했던 키탭파일을 기반으로 tgt티켓이 정상인지 판단함

Keytab 파일 생성 및 배포:
Kerberos 서버에서 각 principal에 대한 keytab 파일을 생성합니다.
이 keytab 파일은 하둡 서버와 클라이언트에 각각 배포하여 인증 과정에서 사용됩니다.

티켓 발급:
클라이언트는 자신의 keytab 파일을 사용하여 Kerberos KDC에서 TGT를 발급받습니다.
클라이언트는 TGT를 사용하여 하둡 서버에 대한 서비스 티켓을 요청합니다.

서비스 티켓 검증:
하둡 서버는 클라이언트가 보낸 서비스 티켓을 자신의 keytab 파일을 사용하여 검증합니다.
검증된 티켓을 기반으로 클라이언트와의 안전한 통신을 설정합니다.

# 하둡 kerberos auth 생략

하둡 접속(kubectl exec -it hadoop~~ -- /bin/bash)
호스트에서 hadoop 그룹 생성
groupadd hadoop && \
 useradd -m -g hadoop hadoop

호스트에서 mynspluto 계정 생성
useradd -m mynspluto && \
 echo 'mynspluto:mynsplutopassword' | chpasswd && \
 usermod -aG hadoop mynspluto

cd ~~/bin
호스트에서 생성된 hadoop 그룹, mynspluto 계정 이미 하둡에도 생성되었음
소유자: mynspluto, 그룹: hadoop
hdfs dfs -chown -R mynspluto:hadoop /

소유자가 7 그룹이 5 일반사용자가 5 권한을 가짐
hdfs dfs -chmod -R 755 /
