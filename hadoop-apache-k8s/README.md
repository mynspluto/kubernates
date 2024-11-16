kubectl logs datanodes-7f467bc4c6-d7nw8

java.io.IOException: Incorrect configuration: namenode address dfs.namenode.servicerpc-address.[] or dfs.namenode.rpc-address.[] is not configured.
at org.apache.hadoop.hdfs.DFSUtil.getNNServiceRpcAddressesForCluster(DFSUtil.java:656)
at org.apache.hadoop.hdfs.server.datanode.BlockPoolManager.refreshNamenodes(BlockPoolManager.java:157)
at org.apache.hadoop.hdfs.server.datanode.DataNode.startDataNode(DataNode.java:1755)
at org.apache.hadoop.hdfs.server.datanode.DataNode.<init>(DataNode.java:564)
at org.apache.hadoop.hdfs.server.datanode.DataNode.makeInstance(DataNode.java:3148)
at org.apache.hadoop.hdfs.server.datanode.DataNode.instantiateDataNode(DataNode.java:3054)
at org.apache.hadoop.hdfs.server.datanode.DataNode.createDataNode(DataNode.java:3098)
at org.apache.hadoop.hdfs.server.datanode.DataNode.secureMain(DataNode.java:3242)
at org.apache.hadoop.hdfs.server.datanode.DataNode.main(DataNode.java:3266)

=> volumeMounts: - name: hadoop-config-volume
mountPath: /opt/hadoop/etc/hadoop
volumes: - name: hadoop-config-volume
configMap:
name: hadoop-config
으로 해결
도커 공식 이미지 레이어를 보니
https://hub.docker.com/layers/apache/hadoop/3.4.1/images/sha256-69ffa97339aff768c4e6120c3fb27aa04c121402b1c8158408a5fb5be586a30e?context=explore
하둡 다운 경로가 /opt/hadoop 이라 /opt/hadoop/etc/hadoop의 컨피그 파일을 교체하면 되었음

org.apache.hadoop.hdfs.server.common.InconsistentFSStateException: Directory /tmp/hadoop-hadoop/dfs/name is in an inconsistent state: storage directory does not exist or is not accessible.
at org.apache.hadoop.hdfs.server.namenode.FSImage.recoverStorageDirs(FSImage.java:392)
at org.apache.hadoop.hdfs.server.namenode.FSImage.recoverTransitionRead(FSImage.java:243)
at org.apache.hadoop.hdfs.server.namenode.FSNamesystem.loadFSImage(FSNamesystem.java:1236)
at org.apache.hadoop.hdfs.server.namenode.FSNamesystem.loadFromDisk(FSNamesystem.java:808)
at org.apache.hadoop.hdfs.server.namenode.NameNode.loadNamesystem(NameNode.java:694)
at org.apache.hadoop.hdfs.server.namenode.NameNode.initialize(NameNode.java:781)
at org.apache.hadoop.hdfs.server.namenode.NameNode.<init>(NameNode.java:1033)
at org.apache.hadoop.hdfs.server.namenode.NameNode.<init>(NameNode.java:1008)
at org.apache.hadoop.hdfs.server.namenode.NameNode.createNameNode(NameNode.java:1782)
at org.apache.hadoop.hdfs.server.namenode.NameNode.main(NameNode.java:1847)
=> hadoop-'hadoop'은 사용한 이미지에서 USER HADOOP 명령어로 user.name을 HADOOP으로 바꿨기 때문에 저 경로에서 찾는것으로 예상
