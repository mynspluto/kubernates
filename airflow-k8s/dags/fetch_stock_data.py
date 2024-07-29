import yfinance as yf
import pandas as pd
from hdfs import InsecureClient
from confluent_kafka import Producer

# 주가 데이터를 수집할 종목 리스트
tickers = ['^IXIC']

# 주가 데이터를 저장할 함수
def fetch_stock_data(ticker):
    local_path = f'./{ticker}.csv'
    stock = yf.Ticker(ticker)
    df = stock.history(period='max')
    df.reset_index(inplace=True)
    df.to_csv(local_path, index=False)
    return local_path

def upload_to_hadoop(local_path, hdfs_path):
    # HDFS 클라이언트 설정
    client = InsecureClient('http://<hadoop-namenode-host>:<port>', user='your_username')

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

# 각 종목의 데이터를 수집하고 HDFS에 업로드
for ticker in tickers:
    local_path = fetch_stock_data(ticker)
    hdfs_path = f'/user/your_username/stock_data/{ticker}.csv'
    #upload_to_hadoop(local_path, hdfs_path)
    #notify_kafka(ticker)
