import os

import yfinance as yf
import pandas as pd
from confluent_kafka import Producer
import requests
from datetime import datetime, timedelta

from airflow import DAG

from airflow.utils.dates import days_ago
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

def upload_to_hadoop(local_path, hdfs_path):
    upload_url = f"{webhdfs_url}{hdfs_path}?op=CREATE&overwrite=true"
    
    with open(local_path, 'rb') as f:
        response = requests.put(upload_url, data=f)
    
    print("response", response)
    
def notify_kafka(ticker):
    kafka_conf = {
        #http://kafkarestproxy.kafka.svc.cluster.local:8082
        'bootstrap.servers': 'http://kafkarestproxy.kafka.svc.cluster.local:9092', 
        'client.id': 'stock-data-producer'
    }
    
    #https://airflow.apache.org/docs/apache-airflow-providers-apache-kafka/stable/_modules/tests/system/providers/apache/kafka/example_dag_hello_kafka.html
    # 참고하여 fetch_stock_data => load_connection => produce => consumer 하면 될듯
    # 9092가 기본포트
    # https://developer.confluent.io/faq/apache-kafka/kafka-operations/
    
    producer = Producer(kafka_conf)
    
    message = f'File for {ticker} has been uploaded to HDFS'
    producer.produce('stock-data-topic', message)
    producer.flush()

with DAG(
    "dag-test",
    default_args={
        "owner": "airflow",
        "depend_on_past": False,
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="Examples of Kafka Operators",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:
    fetch_stock_task = PythonOperator(
        task_id="fetch_stock_data",
        python_callable=fetch_stock_data,
        op_args=['/opt/airflow/stock_data', tickers],  # 로컬 경로와 티커 리스트를 인자로 전달
    )

    
    fetch_stock_data
    
# for ticker in tickers:
#     local_path = f'/opt/airflow/stock_data/asd.csv'
#     fetch_stock_data(local_path, ticker)
#     upload_to_hadoop(local_path, f'/{ticker}.csv')
    #notify_kafka(ticker)

# # 각 종목의 데이터를 수집하고 HDFS에 업로드
# for ticker in tickers:
#     # 첫 번째 작업: 주가 데이터를 수집
#     fetch_task = PythonOperator(
#         task_id=f'fetch_{ticker}_data',
#         python_callable=fetch_stock_data,
#         op_args=[ticker],
#         dag=dag,
#     )

#     # 두 번째 작업: HDFS에 업로드
#     upload_task = PythonOperator(
#         task_id=f'upload_{ticker}_data_to_hdfs',
#         python_callable=upload_to_hadoop,
#         op_args=[f'../stock_data/{ticker}.csv', f'/user/your_username/stock_data/{ticker}.csv'],
#         dag=dag,
#     )

#     # 세 번째 작업: Kafka에 알림 전송
#     notify_task = PythonOperator(
#         task_id=f'notify_kafka_{ticker}',
#         python_callable=notify_kafka,
#         op_args=[ticker],
#         dag=dag,
#     )

#     # 의존성 설정
#     fetch_task >> upload_task >> notify_task
