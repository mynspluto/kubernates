export LANG=en_US.UTF-8
export HADOOP_OS_TYPE=${HADOOP_OS_TYPE:-$(uname -s)}

export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-arm64"
export HDFS_NAMENODE_USER=root
export HDFS_SECONDARYNAMENODE_USER=root
export HDFS_DATANODE_USER=root
export YARN_RESOURCEMANAGER_USER=root
export YARN_NODEMANAGER_USER=root