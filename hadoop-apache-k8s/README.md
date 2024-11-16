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
