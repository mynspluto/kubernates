# kubectl exec -it hadoop-0 -- /bin/bash
# bash-4.2$ cd bin/
# bash-4.2$ hdfs dfs -chmod -R 777 /

POD_NAME="hadoop-0" # 대상 Hadoop Pod 이름
NAMESPACE="default" # Kubernetes 네임스페이스 (필요하면 수정)
HDFS_COMMAND="hdfs dfs -chmod -R 777 /" # 실행할 HDFS 명령어

echo "Executing HDFS command in pod $POD_NAME..."

kubectl exec -it "$POD_NAME" -- /bin/bash -c "cd bin && $HDFS_COMMAND"

curl -i 'http://localhost:9870/webhdfs/v1/?op=LISTSTATUS'
curl -i -X PUT 'http://localhost:9870/webhdfs/v1/airflow/test_data?op=MKDIRS'
# 9870으로 요청시 9864로 리다이렉트 하는 과정에서 hadoop파드 내의 localhost(hadoop-0):9864로 리다이렉트하여 맥 호스트 환경에서는 요청이 불가능한듯 함
curl -i -X PUT -T ./hadoop/test_file.txt 'http://localhost:9864/webhdfs/v1/airflow/test_data/test_file.txt?op=CREATE&namenoderpcaddress=localhost:9000&overwrite=true'

# https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/hdfs-default.xml
# dfs.namenode.http-address 설정필요?
# dfs.datanode.http.address 설정필요?