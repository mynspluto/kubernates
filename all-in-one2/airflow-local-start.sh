#!/usr/bin/env zsh

# kubectl create namespace airflow
# kubectl config set-context --current --namespace=airflow

# eval $(minikube -p minikube docker-env)
# docker build -t mynspluto-airflow:latest -f ./airflow/Dockerfile ./airflow

# helm repo add airflow-stable https://airflow-helm.github.io/charts
# helm repo add apache-airflow https://airflow.apache.org
# helm repo update
# helm install airflow apache-airflow/airflow -n airflow -f ./airflow/values.yml

# Port to forward
# PORT=8080

# # Check if the port is in use and get the PID
# PID=$(lsof -t -i :$PORT)

# # If the port is in use, kill the process
# if [ -n "$PID" ]; then
#     echo "Port $PORT is already in use by PID $PID. Terminating the process..."
#     kill $PID
#     sleep 2  # Wait for the process to terminate
# fi

rm -rf ~/airflow/dags
rm -rf ~/airflow/logs
mkdir -p ~/airflow/dags

#cp -r ./airflow-local/dags/* ~/airflow/dags
cp ./airflow-local/dags/3.py ~/airflow/dags/3.py

pwd

python3 -m venv ./airflow-local/airflow_env
source ./airflow-local/airflow_env/bin/activate
pip install -r ./airflow-local/requirements.txt
airflow standalone

nohup kubectl port-forward svc/airflow-webserver $PORT:$PORT -n airflow > port-forward.log 2>&1 &
