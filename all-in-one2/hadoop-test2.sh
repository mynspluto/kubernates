#kubectl exec -it hadoop-0 -n hadoop -- hdfs dfs -rm /airflow/test_data/test_file.txt

#kubectl cp hadoop/test_file.txt hadoop-0:/tmp/test_file.txt -n hadoop

#kubectl exec -it hadoop-0 -n hadoop -- hdfs dfs -mkdir -p /airflow/test_data
curl -i -L -X PUT -T ./hadoop/test_file.txt 'http://localhost:9870/webhdfs/v1/airflow/test_data/test_file.txt?op=CREATE&overwrite=true'
#kubectl exec -it hadoop-0 -n hadoop -- hdfs dfs -ls /airflow/test_data/
#kubectl exec -it hadoop-0 -n hadoop -- hdfs dfs -cat /airflow/test_data/test_file.txt
