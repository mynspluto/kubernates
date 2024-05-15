하둡 공식 사이트에서 하둡 바이너리 압축파일 받아서 아래와 같은 Dockerfile 생성(데이터노드, 네임노드, 리소스매니저 가각 생성 => 맨 밑의 cmd만 바꾸면 된다?)

# Dockerfile

# 베이스 이미지 설정 (Ubuntu 기반 이미지 사용)

FROM ubuntu:latest

# 로컬에 있는 하둡 압축 파일을 이미지로 복사

COPY hadoop-3.2.2.tar.gz /tmp/

# 하둡 압축 해제 및 설치

RUN tar -xzvf /tmp/hadoop-3.2.2.tar.gz -C /usr/local/ && \
 mv /usr/local/hadoop-3.2.2 /usr/local/hadoop

# 필요한 설정 파일 복사

COPY core-site.xml /usr/local/hadoop/etc/hadoop/
COPY hdfs-site.xml /usr/local/hadoop/etc/hadoop/
COPY mapred-site.xml /usr/local/hadoop/etc/hadoop/
COPY yarn-site.xml /usr/local/hadoop/etc/hadoop/

# 하둡 환경 변수 설정

ENV HADOOP_HOME /usr/local/hadoop
ENV PATH $HADOOP_HOME/bin:$PATH

# 마지막으로 컨테이너에서 실행될 명령

CMD ["bash"]

CMD ["hadoop-daemon.sh start namenode"]
CMD ["hadoop-daemon.sh start datanode"]
