kubectl cp ./test_file.txt namenode-54d7895df-k4ck5:/tmp/test_file.txt -n hadoop

kubectl exec -it namenode-54d7895df-k4ck5 -- hdfs dfs -mkdir -p /airflow/test_data
kubectl exec -it namenode-54d7895df-k4ck5 -- hdfs dfs -put /tmp/test_file.txt /airflow/test_data/test_file.txt
kubectl exec -it namenode-54d7895df-k4ck5 -- hdfs dfs -ls /airflow/test_data/
kubectl exec -it namenode-54d7895df-k4ck5 -- hdfs dfs -cat /airflow/test_data/test_file.txt

아마도 하둡 권장 사양이 메모리 16이상이라
kubectl cp ./test_file.txt namenode-54d7895df-k4ck5:/tmp/test_file.txt -n hadoop 이게 간헐적으로 실패하는듯함
kubectl top 가능하게 세팅 (minikube start 옵션에 있는듯)
resources.requests, limit 메모리 올리기

hdfs dfs -mkdir -p /user/root
hdfs dfs -chown root /user/root
hdfs dfs -chmod -R 770 /user/root

kubectl exec -it namenode-54d7895df-k4ck5 -- /bin/bash
$HADOOP_HOME/bin/hdfs dfs -chmod -R 777 /

kubectl exec -it airflow-webserver -- /bin/bash
python fetch_stock_data.py

kubectl exec -it namenode-54d7895df-k4ck5 -- /bin/bash
$HADOOP_HOME/bin/hdfs dfs -ls /
