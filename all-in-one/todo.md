1. start, stop, restart sh 작성

2. 카프카 start.sh stop.sh, t1(producer), t2(consumer): upload to hadoop
   start.kafka.sh 클러스터 주소 가져와서 토픽 생성하는 부분 따로 빼야할듯
   => t1에서 토픽 가져와서 리스트 보고 없으면 생성
   stop.sh후 start.sh하면 confluent-operator-745b699c76-6gj8g만 생성되고 그 뒤로 나머지 파드 생성안됨 다시 stop후 start하면 생성됨 원인 모름 pod지워지는걸 끝까지 안기다려서 그런가?

3. 하둡 start.sh stop.sh t3(download at hadoop)

4. dag t1, t2, t3 작성
   airflow dag t1(producer) t2(consumer)
   producer에서 consumer에게 신호 보냄
   consumer는 신호를 받고 하둡을 통해 주가 데이터 다운로드
   t1 => t2 데이터 전처리하여 하둡에 업로드 => t3 하둡에서 전처리된 데이터 다운 후 머신러닝

hadoop dockerfile amd64 arm64 분기처리

[hadoop 파일 업로드 403 에러]
cd /usr/local/hadoop/bin
hdfs dfs -chmod -R 777 /

[airflow kafka ProduceToTopicOperator 토픽 없음 에러]
airflow@airflow-worker-0:/opt/airflow/logs$ cd 'dag_id=dag-test'/
airflow@airflow-worker-0:/opt/airflow/logs/dag_id=dag-test$ ls
'run_id=manual**2024-11-09T06:10:52.151099+00:00' 'run_id=scheduled**2024-11-09T00:00:00+00:00'
airflow@airflow-worker-0:/opt/airflow/logs/dag_id=dag-test$ cd 'run_id=scheduled**2024-11-09T00:00:00+00:00'
airflow@airflow-worker-0:/opt/airflow/logs/dag_id=dag-test/run_id=scheduled**2024-11-09T00:00:00+00:00$ ls
'task_id=fetch_stock_data_task' 'task_id=load_connections' 'task_id=produce_to_topic' 'task_id=upload_to_hadoop_task'
airflow@airflow-worker-0:/opt/airflow/logs/dag_id=dag-test/run_id=scheduled**2024-11-09T00:00:00+00:00$ cd 'task_id=produce_to_topic'/
airflow@airflow-worker-0:/opt/airflow/logs/dag_id=dag-test/run_id=scheduled**2024-11-09T00:00:00+00:00/task_id=produce_to_topic$ ls
'attempt=1.log' 'attempt=2.log'
airflow@airflow-worker-0:/opt/airflow/logs/dag_id=dag-test/run_id=scheduled**2024-11-09T00:00:00+00:00/task_id=produce_to_topic$ tail -f attempt\=2.log
return func(self, \*args, \*\*kwargs)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/home/airflow/.local/lib/python3.12/site-packages/airflow/providers/apache/kafka/operators/produce.py", line 126, in execute
producer.produce(self.topic, key=k, value=v, on_delivery=self.delivery_callback)
cimpl.KafkaException: KafkaError{code=\_UNKNOWN_TOPIC,val=-188,str="Unable to produce message: Local: Unknown topic"}
[2024-11-10T05:35:21.956+0000] {taskinstance.py:1206} INFO - Marking task as FAILED. dag_id=dag-test, task_id=produce_to_topic, run_id=scheduled**2024-11-09T00:00:00+00:00, execution_date=20241109T000000, start_date=20241110T053451, end_date=20241110T053521
[2024-11-10T05:35:21.963+0000] {standard_task_runner.py:110} ERROR - Failed to execute job 34 for task produce_to_topic (KafkaError{code=\_UNKNOWN_TOPIC,val=-188,str="Unable to produce message: Local: Unknown topic"}; 121)
[2024-11-10T05:35:21.994+0000] {local_task_job_runner.py:240} INFO - Task exited with return code 1

hadoop => hadoop-apache-k8s
kafka => kafka-native-k8s
교체

hadoop, kafka는 k8s로 켜 놓은 상태에서
airflow만 로컬 실행, dag git으로 동기화 하여 dag적용 간소화
