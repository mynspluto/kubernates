import os
import yfinance as yf
import requests
from datetime import datetime, timedelta
import logging

webhdfs_url = 'http://localhost:9870/webhdfs/v1'

# 주가 데이터를 저장할 함수
def fetch_stock_data(local_path, tickers):
    try:
        # 디렉토리 생성 여부 확인
        if not os.path.exists(local_path):
            os.makedirs(local_path)
            logging.info(f"Directory created: {local_path}")
        
        for ticker in tickers:
            try:
                logging.info(f"Fetching data for ticker: {ticker}")
                stock = yf.Ticker(ticker)
                df = stock.history(period='max')
                if df.empty:
                    logging.warning(f"No data found for ticker: {ticker}")
                    continue
                df.reset_index(inplace=True)
                # 각 티커의 데이터를 별도의 파일로 저장
                file_path = f"{local_path}/{ticker}.csv"
                df.to_csv(file_path, index=False)
                logging.info(f"Data saved to: {file_path}")
            except Exception as e:
                logging.error(f"Failed to fetch or save data for {ticker}: {e}", exc_info=True)
    except Exception as e:
        logging.critical(f"Unexpected error occurred: {e}", exc_info=True)

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
                "bootstrap.servers": "localhost:9092"}),
        )
    )
    
    db.merge_conn(
        Connection(
            conn_id="t2",
            conn_type="kafka",
            extra=json.dumps(
                {
                    "bootstrap.servers": "localhost:9092",
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

    

    
tickers = ['^IXIC']
fetch_stock_data('./data', tickers)
#>> upload_to_hadoop_task >> t0 >> t1 >> t2
