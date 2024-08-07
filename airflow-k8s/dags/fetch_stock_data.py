from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import yfinance as yf
import pandas as pd
from hdfs import InsecureClient
from confluent_kafka import Producer

# 주가 데이터를 수집할 종목 리스트
tickers = ['^IXIC']

# 주가 데이터를 저장할 함수
def fetch_stock_data(ticker):
    local_path = f'/opt/airflow/stock_data/{ticker}.csv'
    stock = yf.Ticker(ticker)
    df = stock.history(period='max')
    df.reset_index(inplace=True)
    df.to_csv(local_path, index=False)
    return local_path

def upload_to_hadoop(local_path, hdfs_path):
    # HDFS 클라이언트 설정
    client = InsecureClient('http://hadoop-service.hadoop:9870')
    
    #client.makedirs('/home/stock_data')
    
    # 파일 업로드
    client.upload(hdfs_path, local_path, overwrite=True)
    
def notify_kafka(ticker):
    kafka_conf = {
        'bootstrap.servers': '<kafka-broker-host>:<port>',
        'client.id': 'stock-data-producer'
    }
    producer = Producer(kafka_conf)
    
    message = f'File for {ticker} has been uploaded to HDFS'
    producer.produce('stock-data-topic', message)
    producer.flush()
    
for ticker in tickers:
    local_path = fetch_stock_data(ticker)
    hdfs_path = f'/opt/airflow/stock_data/{ticker}.csv'
    upload_to_hadoop(local_path, hdfs_path)
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
