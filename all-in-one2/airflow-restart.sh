rm -rf ~/airflow/dags
mkdir -p ~/airflow/dags

#cp -r ./airflow-local/dags/* ~/airflow/dags
cp ./airflow-local/dags/3.py ~/airflow/dags/3.py

source ./airflow-local/airflow_env/bin/activate
pip install -r ./airflow-local/requirements.txt
airflow standalone