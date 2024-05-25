# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND noninteractive
ENV HADOOP_VERSION=3.4.0
ENV HADOOP_HOME=/usr/local/hadoop

# Install necessary packages
RUN apt-get update && \
    apt-get install -y wget openjdk-8-jdk ssh pdsh rsync && \
    apt-get clean

RUN echo $(which java)
RUN ls -al /usr/lib
RUN ls -al /usr/lib/jvm
RUN ls -al /usr/lib/jvm/java-8-openjdk-arm64
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV PATH=$PATH:$JAVA_HOME/bin
# Verify Java installation
RUN echo "JAVA_HOME is set to $JAVA_HOME" && \
    ls -la $JAVA_HOME

# Download and extract Hadoop
RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}-aarch64.tar.gz && \
    tar -xzvf hadoop-${HADOOP_VERSION}-aarch64.tar.gz && \
    mv hadoop-${HADOOP_VERSION} $HADOOP_HOME && \
    rm hadoop-${HADOOP_VERSION}-aarch64.tar.gz

ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

# Copy the start script
COPY config/start-hadoop.sh /usr/local/bin/start-hadoop.sh
RUN chmod +x /usr/local/bin/start-hadoop.sh

RUN mkdir -p $HADOOP_HOME/data/dfs/namenode&& \
    mkdir -p $HADOOP_HOME/data/dfs/datanode&& \
    chmod -R 755 $HADOOP_HOME/data/dfs

# Configure SSH
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys && \
    echo "Host *\n    StrictHostKeyChecking no\n" >> /etc/ssh/ssh_config

# Expose necessary ports
EXPOSE 9870 9864 8088 8042

# Start SSH service and Hadoop
CMD ["/usr/local/bin/start-hadoop.sh"]
