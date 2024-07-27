from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import yfinance as yf
import pandas as pd

# 주가 데이터를 수집할 종목 리스트
tickers = ['AAPL', 'GOOGL', 'MSFT']

# 주가 데이터를 저장할 함수
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period='1d')
    df.reset_index(inplace=True)
    df.to_csv(f'/path/to/save/{ticker}.csv', index=False)

# DAG 정의
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
}

dag = DAG(
    'fetch_stock_data',
    default_args=default_args,
    description='Fetch stock data from Yahoo Finance',
    schedule_interval='@daily',
)

# PythonOperator를 사용하여 각 종목의 데이터를 수집
for ticker in tickers:
    task = PythonOperator(
        task_id=f'fetch_{ticker}_data',
        python_callable=fetch_stock_data,
        op_args=[ticker],
        dag=dag,
    )
