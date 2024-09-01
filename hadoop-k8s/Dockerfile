# Use the official Ubuntu base image
FROM ubuntu:20.04

# Set environment variables
ENV DEBIAN_FRONTEND noninteractive
ENV HADOOP_VERSION=3.4.0
ENV HADOOP_HOME=/usr/local/hadoop

# Install necessary packages
RUN apt-get update && \
    apt-get install -y vim wget openjdk-8-jdk ssh pdsh rsync sudo openssh-server net-tools curl && \
    apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64
ENV PATH=$PATH:$JAVA_HOME/bin

# Verify Java installation
RUN echo "JAVA_HOME is set to $JAVA_HOME" && \
    ls -la $JAVA_HOME

# 하둡 설치 - 1.web에서 가져오기 or 2.로컬에서 가져오기 둘 중 하나 선택
# hadoop 설치 방법 - 1.web에서 가져오기
# RUN wget https://downloads.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}-aarch64.tar.gz && \
#     tar -xzvf hadoop-${HADOOP_VERSION}-aarch64.tar.gz && \
#     mv hadoop-${HADOOP_VERSION} $HADOOP_HOME && \
#     rm hadoop-${HADOOP_VERSION}-aarch64.tar.gz

# 하둡 설치 - 2.로컬에 있는 hadoop tar.gz 파일을 컨테이너에 복사
COPY hadoop-${HADOOP_VERSION}-aarch64.tar.gz /tmp/

# 이후에 tar.gz 파일을 사용하여 Hadoop 설치
RUN tar -xzvf /tmp/hadoop-${HADOOP_VERSION}-aarch64.tar.gz && \
    mv hadoop-${HADOOP_VERSION} $HADOOP_HOME && \
    rm /tmp/hadoop-${HADOOP_VERSION}-aarch64.tar.gz

ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

COPY config/hadoop-env.sh ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh
RUN chmod +x ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

COPY config/hadoop-functions.sh ${HADOOP_HOME}/libexec/hadoop-functions.sh
RUN chmod +x ${HADOOP_HOME}/libexec/hadoop-functions.sh

COPY config/core-site.xml ${HADOOP_HOME}/etc/hadoop/core-site.xml
RUN chmod +x ${HADOOP_HOME}/etc/hadoop/core-site.xml

COPY config/core-site.xml ${HADOOP_HOME}/etc/hadoop/hdfs-site.xml
RUN chmod +x ${HADOOP_HOME}/etc/hadoop/hdfs-site.xml

# COPY config/hdfs-default.xml ${HADOOP_HOME}/etc/hadoop/hdfs-default.xml
# RUN chmod +x ${HADOOP_HOME}/etc/hadoop/hdfs-default.xml

RUN mkdir -p $HADOOP_HOME/data/dfs/namenode && \
    mkdir -p $HADOOP_HOME/data/dfs/datanode && \
    chmod -R 777 $HADOOP_HOME

# Configure SSH
RUN $HADOOP_HOME/bin/hdfs namenode -format

# 3. SSH 서버 디렉토리 생성
RUN mkdir /var/run/sshd

# 4. root 계정 비밀번호 설정 (보안상 매우 위험, 실제로 사용할 때는 주의 필요)
RUN echo 'root:rootpassword' | chpasswd

# 5. PermitRootLogin 설정 (보안상 위험, 테스트용으로만 사용 권장)
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys && \
    echo "Host *\n    StrictHostKeyChecking no\n" >> /etc/ssh/ssh_config

# Hadoop 사용자 및 그룹 생성
RUN groupadd hadoop && \
    useradd -m -g hadoop hadoop

# 사용자 생성 및 비밀번호 설정
RUN useradd -m mynspluto && \
    echo 'mynspluto:mynsplutopassword' | chpasswd && \
    usermod -aG hadoop mynspluto

# 권한 부여
RUN chown -R hadoop:hadoop $HADOOP_HOME && \
    chmod -R 755 $HADOOP_HOME

# Expose necessary ports
EXPOSE 22 9870 9864 8088 8042

# Start SSH service and Hadoop
# 9. SSH 및 Hadoop DFS 시작
CMD sh -c "/usr/sbin/sshd && export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-arm64 && $HADOOP_HOME/sbin/start-dfs.sh && tail -f /dev/null"
