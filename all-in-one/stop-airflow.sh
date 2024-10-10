helm uninstall airflow -n airflow
kubectl delete all --all -n airflow
kubectl delete namespace airflow