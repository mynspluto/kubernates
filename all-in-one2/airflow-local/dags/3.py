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

local_path = '~/airflow/stock_data'
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
    
    fetch_stock_task
    #>> upload_to_hadoop_task >> t0 >> t1 >> t2
