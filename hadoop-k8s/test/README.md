kubectl cp ./test_file.txt hadoop-deployment-97d574559-kxbnn:/tmp/test_file.txt -n hadoop

kubectl exec -it hadoop-deployment-97d574559-kxbnn -- bin/bash hadoop namenode -format
kubectl exec -it hadoop-deployment-97d574559-kxbnn -- hdfs dfs -mkdir -p /airflow/test_data
kubectl exec -it hadoop-deployment-97d574559-kxbnn -- hdfs dfs -put /tmp/test_file.txt /airflow/test_data/test_file.txt
