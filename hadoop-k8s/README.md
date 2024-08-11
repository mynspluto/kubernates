kubectl create namespace hadoop
kubectl config set-context --current --namespace=hadoop
docker system prune -a

kubectl delete all --all -n hadoop (pv, pvc는 안지워짐)
kubectl delete pvc --all -n hadoop
kubectl delete pv hadoop-pv

minikube ssh
docker rmi hadoop
docker build -t hadoop:latest .
minikube image load hadoop:latest

kubectl apply -f svc.yml --namespace=hadoop
kubectl apply -f one.yml --namespace=hadoop

kubectl get endpoints -n hadoop

kubectl port-forward service/hadoop-service 9870(port: 1234면 1234, 9870이라 9870인거임)

vim /usr/local/hadoop/etc/hadoop/core-site.xml
$HADOOP_HOME/sbin/stop-all.sh
$HADOOP_HOME/bin/hadoop namenode -format
$HADOOP_HOME/sbin/start-all.sh

TODO
https://hadoop.apache.org/docs/r3.0.0/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml

dfs.namenode.rpc-address주소, 포트랑 쿠버네티스 서비스 연결시켜서
클라이언트에서 연결시 그 주소로 해야 될 것으로 추측

fs.defaultFS를 hdfs://hadoop-service.hadoop.svc.cluster.local:9870으로 하였을때
ssh 연결안되는에러 service에 22번포트 expose하여 해결

core-site.xml의 fs.defaultFS를 9867로 연결시켜야할거같음
=> 도커 재빌드, 쿠버네티스 요소 재실행후 확인
