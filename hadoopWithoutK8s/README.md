hadoop-env.sh의 JAVA_HOME이 ~/Library/Java/JavaVirtualMachines/corretto-1.8.0_402/Contents/Home일 때 한동안 resource 생성안됐음

~/.zshrc에 HADOOP_HOME 설정

jps

ssh localhost
hadoop namenode -format
start-all.sh
stop-all.sh

Cluster status : http://localhost:8088
HDFS status : http://localhost:9870
Secondary NameNode status : http://localhost:9868

in chris
hdfs dfs -mkdir -p /user/mynspluto
hdfs dfs -chown -R mynspluto /user/mynspluto
hdfs dfs -chmod -R 770 /user/mynspluto

in mynspluto
hadoop fs -put ./hadoopWithoutK8s/README.md
hadoop fs -get README.md
hadoop fs -ls /Users/mynspluto
