kubectl cp hadoop/test_file.txt hadoop-0:/tmp/test_file.txt -n hadoop

kubectl exec -it hadoop-0 -n hadoop -- hdfs dfs -mkdir -p /airflow/test_data
kubectl exec -it hadoop-0 -n hadoop -- hdfs dfs -put /tmp/test_file.txt /airflow/test_data/test_file.txt
kubectl exec -it hadoop-0 -n hadoop -- hdfs dfs -ls /airflow/test_data/
kubectl exec -it hadoop-0 -n hadoop -- hdfs dfs -cat /airflow/test_data/test_file.txt
