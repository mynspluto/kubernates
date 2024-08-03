#!/bin/bash

service ssh start

if [ "$HADOOP_ROLE" == "namenode" ]; then
    if [ ! -d "$HADOOP_HOME/data/dfs/namenode/current" ]; then
        echo "Formatting NameNode..."
        hdfs namenode -format -nonInteractive
    fi
    $HADOOP_HOME/bin/hdfs namenode
elif [ "$HADOOP_ROLE" == "datanode" ]; then
    $HADOOP_HOME/bin/hdfs datanode
else
    echo "Unknown role: $HADOOP_ROLE"
    exit 1
fi
