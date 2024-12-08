import os
import yfinance as yf
import pandas as pd
from confluent_kafka import Producer
import json
import requests
from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from airflow.operators.python import PythonOperator
from airflow.providers.apache.kafka.operators.consume import ConsumeFromTopicOperator
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
from airflow.providers.apache.kafka.sensors.kafka import AwaitMessageSensor

webhdfs_url = 'http://hadoop-service.hadoop.svc.cluster.local:9870/webhdfs/v1'

# 주가 데이터를 수집할 종목 리스트
tickers = ['^IXIC']

# 주가 데이터를 저장할 함수
def fetch_stock_data(local_path, tickers):
    if not os.path.exists(local_path):
        os.makedirs(local_path)
        
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        df = stock.history(period='max')
        df.reset_index(inplace=True)
        # 각 티커의 데이터를 별도의 파일로 저장
        df.to_csv(f"{local_path}/{ticker}.csv", index=False)

# HDFS에 파일 업로드 함수
# kubectl exec -it hadoop-statefulset-0 -- /bin/bash
# $HADOOP_HOME/bin/hdfs dfs -chmod -R 777 /
def upload_to_hadoop(local_path):
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            # HDFS 경로 생성
            relative_path = os.path.relpath(local_file_path, local_path)
            hdfs_file_path = os.path.join(relative_path)
            upload_url = f"{webhdfs_url}/{hdfs_file_path}?op=CREATE&overwrite=true"
            
            with open(local_file_path, 'rb') as f:
                response = requests.put(upload_url, data=f)
            
            print(f"Uploaded {local_file_path} to {hdfs_file_path}, response: {response}")

def load_connections():
    # Connections needed for this example dag to finish
    from airflow.models import Connection
    from airflow.utils import db

    db.merge_conn(
        Connection(
            conn_id="t1",
            conn_type="kafka",
            extra=json.dumps({
                "socket.timeout.ms": 10, 
                "bootstrap.servers": "kafka.kafka.svc.cluster.local:9092"}),
        )
    )
    
    db.merge_conn(
        Connection(
            conn_id="t2",
            conn_type="kafka",
            extra=json.dumps(
                {
                    "bootstrap.servers": "kafka.kafka.svc.cluster.local:9092",
                    "group.id": "t2",
                    "enable.auto.commit": False,
                    "auto.offset.reset": "beginning",
                }
            ),
        )
    )

def producer_function():
    for i in range(20):
        yield (json.dumps(i), json.dumps(i + 1))
        
def consumer_function(message, prefix=None):
    key = json.loads(message.key())
    value = json.loads(message.value())
    print("%s %s @ %s; %s : %s", prefix, message.topic(), message.offset(), key, value)
    return

    
with DAG(
    "predict-stock",
    default_args={
        "owner": "airflow",
        "depend_on_past": False,
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 0,
        "retry_delay": timedelta(minutes=5),
    },
    description="Examples of Kafka Operators",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:
    fetch_stock_task = PythonOperator(
        task_id="fetch_stock_data_task",
        python_callable=fetch_stock_data,
        op_args=['/opt/airflow/stock_data', tickers],  # 로컬 경로와 티커 리스트를 인자로 전달
    )
    
    upload_to_hadoop_task = PythonOperator(
        task_id="upload_to_hadoop_task",
        python_callable=upload_to_hadoop,
        op_args=['/opt/airflow/stock_data'],  # 로컬 경로와 티커 리스트를 인자로 전달
    )
    
    t0 = PythonOperator(task_id="load_connections", python_callable=load_connections)
    
    t1 = ProduceToTopicOperator(
        kafka_config_id="t1",
        task_id="produce_to_topic",
        topic="test_1",
        producer_function="fetch_stock_data.producer_function",
    )
    
    t2 = ConsumeFromTopicOperator(
        kafka_config_id="t2",
        task_id="consume_from_topic",
        topics=["test_1"],
        apply_function="fetch_stock_data.consumer_function",
        apply_function_kwargs={"prefix": "consumed:::"},
        commit_cadence="end_of_batch",
        max_messages=10,
        max_batch_size=2,
    )
    
    
    fetch_stock_task >> upload_to_hadoop_task >> t0 >> t1 >> t2
