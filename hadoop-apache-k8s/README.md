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
