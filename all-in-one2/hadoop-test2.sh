nohup kubectl port-forward svc/hadoop-service 9864:9864 -n hadoop > port-forward.log 2>&1 &
#curl -i 'http://localhost:9870/webhdfs/v1/?op=LISTSTATUS'

# 403
curl -i -X PUT 'http://localhost:9870/webhdfs/v1/airflow/test_data?op=MKDIRS'


# kubectl exec -it hadoop-0 -- /bin/bash
# bash-4.2$ cd bin/
# bash-4.2$ hdfs dfs -chmod -R 777 /
curl -i -X PUT -T ./hadoop/test_file.txt 'http://localhost:9864/webhdfs/v1/airflow/test_data/test_file.txt?op=CREATE&namenoderpcaddress=localhost:9000&overwrite=true'


