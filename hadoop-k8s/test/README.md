kubectl cp ./test_file.txt hadoop-pod:/tmp/test_file.txt -n hadoop

kubectl exec -it hadoop-pod -- bin/bash hadoop namenode -format
kubectl exec -it hadoop-pod -- hdfs dfs -mkdir -p /airflow/test_data
kubectl exec -it hadoop-pod -- hdfs dfs -put /tmp/test_file.txt /airflow/test_data/test_file.txt
kubectl exec -it hadoop-pod -- hdfs dfs -ls /airflow/test_data/
kubectl exec -it hadoop-pod -- hdfs dfs -cat /airflow/test_data/test_file.txt

아마도 하둡 권장 사양이 메모리 16이상이라
kubectl cp ./test_file.txt hadoop-pod:/tmp/test_file.txt -n hadoop 이게 간헐적으로 실패하는듯함
kubectl top 가능하게 세팅 (minikube start 옵션에 있는듯)
resources.requests, limit 메모리 올리기
