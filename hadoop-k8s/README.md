# 네임스페이스 생성 및 변경

kubectl create namespace hadoop
kubectl config set-context --current --namespace=hadoop

# 기존 요소 제거

kubectl delete all --all -n hadoop (pv, pvc는 안지워짐)
kubectl delete pvc --all -n hadoop
kubectl delete pv hadoop-pv
docker system prune -a

minikube ssh
docker rmi hadoop

# 이미지 생성, 이미지 로드

docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.CreatedAt}}"
docker build -t hadoop:latest .

# 요소 생성, 서비스 포워딩

kubectl apply -f svc.yml --namespace=hadoop
kubectl apply -f one.yml --namespace=hadoop

kubectl get endpoints -n hadoop
kubectl port-forward service/hadoop-service 9870(port: 1234면 1234, 9870이라 9870인거임)

# 테스트

kubectl cp ./test_file.txt hadoop-statefulset-0:/tmp/test_file.txt -n hadoop

kubectl exec -it hadoop-statefulset-0 -- hdfs dfs -mkdir -p /airflow/test_data
kubectl exec -it hadoop-statefulset-0 -- hdfs dfs -put /tmp/test_file.txt /airflow/test_data/test_file.txt
kubectl exec -it hadoop-statefulset-0 -- hdfs dfs -ls /airflow/test_data/
kubectl exec -it hadoop-statefulset-0 -- hdfs dfs -cat /airflow/test_data/test_file.txt

# 수동 하둡실행

vim /usr/local/hadoop/etc/hadoop/core-site.xml
$HADOOP_HOME/sbin/stop-all.sh
$HADOOP_HOME/bin/hadoop namenode -format
$HADOOP_HOME/sbin/start-all.sh

# 리소스 사용량

NAME CPU(cores) MEMORY(bytes)  
hadoop-statefulset-0 17m 705Mi

NAME CPU(cores) CPU% MEMORY(bytes) MEMORY%  
minikube 221m 2% 1701Mi 7%

TODO
https://hadoop.apache.org/docs/r3.0.0/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml

dfs.namenode.rpc-address주소, 포트랑 쿠버네티스 서비스 연결시켜서
클라이언트에서 연결시 그 주소로 해야 될 것으로 추측

fs.defaultFS를 hdfs://hadoop-service.hadoop.svc.cluster.local:9870으로 하였을때
ssh 연결안되는에러 service에 22번포트 expose하여 해결

core-site.xml의 fs.defaultFS를 9867로 연결시켜야할거같음
=> 도커 재빌드, 쿠버네티스 요소 재실행후 확인
