helm upgrade airflow apache-airflow/airflow -n airflow -f values.yml

kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow

id: admin
pw: admin
