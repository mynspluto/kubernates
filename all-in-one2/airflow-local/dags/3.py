import os
import yfinance as yf
import pandas as pd
from confluent_kafka import Producer
import json
import requests
from datetime import datetime, timedelta
import logging


from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from airflow.operators.python import PythonOperator
from airflow.providers.apache.kafka.operators.consume import ConsumeFromTopicOperator
from airflow.providers.apache.kafka.operators.produce import ProduceToTopicOperator
from airflow.providers.apache.kafka.sensors.kafka import AwaitMessageSensor

# 현재 터미널 세션기준으로 상대 위치 정해지는듯 함
local_path = '/home/mynspluto/airflow'
webhdfs_url = 'http://localhost:9870/webhdfs/v1'

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
        df.to_csv(f"{local_path}/{ticker}.csv", index=False)
        
def upload_to_hadoop(local_path):
    logging.info(f"local_path {local_path}")
    try:
        for root, dirs, files in os.walk(local_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, local_path)
                hdfs_file_path = f"/{relative_path}"  # HDFS 경로
                upload_url = f"{webhdfs_url}{hdfs_file_path}?op=CREATE&overwrite=true"
                
                logging.info(f"Uploading file: {local_file_path} to URL: {upload_url}")
                
                with open(local_file_path, 'rb') as f:
                    response = requests.put(upload_url, data=f)
                    logging.info(f"Uploaded {local_file_path} to {hdfs_file_path}, Response: {response.status_code}")
    except Exception as e:
        logging.error(f"Failed to upload {local_file_path}: {e}")
        raise

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
        task_id="fetch_stock_data_task",
        python_callable=fetch_stock_data,
        op_args=[local_path, tickers],  # 로컬 경로와 티커 리스트를 인자로 전달
    )
    
    upload_to_hadoop_task = PythonOperator(
        task_id="upload_to_hadoop_task",
        python_callable=upload_to_hadoop,
        op_args=[local_path],
    )
    
    fetch_stock_task >> upload_to_hadoop_task
    #>> t0 >> t1 >> t2
