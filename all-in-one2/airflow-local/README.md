## 파이썬 설치

sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv

## 가상환경 생성, 활성화

python3 -m venv airflow_env
source airflow_env/bin/activate

## airflow 환경 변수 설정

export AIRFLOW_HOME=~/airflow

## airflow 가상환경에 설치

pip install apache-airflow

## airflow 디비(postgres, celery) 설치

pip install 'apache-airflow[postgres,celery]'

## db 초기화

airflow db init

## 계정 생성

airflow users create \
 --username admin \
 --firstname Admin \
 --lastname User \
 --role Admin \
 --email admin@example.com

## 웹 서버 실행

airflow webserver -p 8080

## 스케줄러 실행

airflow scheduler

## db 지우기

cd ~/airflow
rm airflow.db
