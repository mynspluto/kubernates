import yfinance as yf
import pandas as pd

# 주가 데이터를 수집할 종목 리스트
tickers = ['AAPL', 'GOOGL', 'MSFT']

# 주가 데이터를 저장할 함수
def fetch_stock_data(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(period='1d')
    df.reset_index(inplace=True)
    df.to_csv(f'./{ticker}.csv', index=False)

# PythonOperator를 사용하여 각 종목의 데이터를 수집
for ticker in tickers:
    fetch_stock_data(ticker)
