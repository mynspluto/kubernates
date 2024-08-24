import os
import yfinance as yf
import pandas as pd
from confluent_kafka import Producer
import requests
from datetime import datetime, timedelta

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

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
        op_args=['/opt/airflow/stock_data', tickers],  # 로컬 경로와 티커 리스트를 인자로 전달
    )
    
    upload_to_hadoop_task = PythonOperator(
        task_id="upload_to_hadoop_task",
        python_callable=upload_to_hadoop,
        op_args=['/opt/airflow/stock_data'],  # 로컬 경로와 티커 리스트를 인자로 전달
    )
    
    fetch_stock_task >> upload_to_hadoop_task
