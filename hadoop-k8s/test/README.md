kubectl cp ./test_file.txt hadoop-namenode-5bbb7f4765-xrmvg:/tmp/test_file.txt -n hadoop

kubectl exec -it hadoop-namenode-5bbb7f4765-xrmvg -n hadoop -- bin/bash hadoop namenode -format
kubectl exec -it hadoop-namenode-5bbb7f4765-xrmvg -n hadoop -- hdfs dfs -mkdir -p /airflow/test_data
kubectl exec -it hadoop-namenode-5bbb7f4765-xrmvg -n hadoop -- hdfs dfs -put /tmp/test_file.txt /airflow/test_data/test_file.txt
