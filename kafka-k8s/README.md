카프카 사용시 주키퍼를 쓰지 않고 kraft를 쓰는 방향으로 추세가 바뀜
=> https://docs.confluent.io/platform/current/installation/docker/config-reference.html

/bin/kafka-storage random-uuid
변수 에 출력을 할당합니다 CLUSTER_ID.

docker run -d \
--name=kafka-kraft \
-h kafka-kraft \
-p 9101:9101 \
-e KAFKA_NODE_ID=1 \
-e KAFKA_LISTENER_SECURITY_PROTOCOL_MAP='CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT' \
-e KAFKA_ADVERTISED_LISTENERS='PLAINTEXT://kafka-kraft:29092,PLAINTEXT_HOST://localhost:9092' \
-e KAFKA_JMX_PORT=9101 \
-e KAFKA_JMX_HOSTNAME=localhost \
-e KAFKA_PROCESS_ROLES='broker,controller' \
-e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
-e KAFKA_CONTROLLER_QUORUM_VOTERS='1@kafka-kraft:29093' \
-e KAFKA_LISTENERS='PLAINTEXT://kafka-kraft:29092,CONTROLLER://kafka-kraft:29093,PLAINTEXT_HOST://0.0.0.0:9092' \
-e KAFKA_INTER_BROKER_LISTENER_NAME='PLAINTEXT' \
-e KAFKA_CONTROLLER_LISTENER_NAMES='CONTROLLER' \
-e CLUSTER_ID='MkU3OEVBNTcwNTJENDM2Qk' \
confluentinc/cp-kafka:7.6.1

cluster_id를 명령어를 통해 생성해야하는데
initContainers:

- name: init-cluster-id
  image: confluentinc/cp-kafka:7.6.1
  command: - "/bin/sh" - "-c" - "export KAFKA_CLUSTER_ID=$(bin/kafka-storage random-uuid) && echo KAFKA_CLUSTER_ID=$KAFKA_CLUSTER_ID"
  env: - name: KAFKA_CLUSTER_ID
  valueFrom:
  configMapKeyRef:
  name: kafka-config
  key: cluster-id
  이런식으로 구현이 가능해보임
