minikube start --cpus 6 --memory 24000 --driver=docker
minikube addons enable metrics-server
minikube docker-env
eval $(minikube -p minikube docker-env)

#helm uninstall airflow -n airflow
#kubectl delete all --all -n airflow

kubectl create namespace airflow
kubectl config set-context --current --namespace=airflow

docker build -t mynspluto-airflow:latest -f ./airflow/Dockerfile ./airflow
helm install airflow apache-airflow/airflow -n airflow -f ./airflow/values.yml

# Port to forward
PORT=8080

# Check if the port is in use and get the PID
PID=$(lsof -t -i :$PORT)

# If the port is in use, kill the process
if [ -n "$PID" ]; then
    echo "Port $PORT is already in use by PID $PID. Terminating the process..."
    kill $PID
    sleep 2  # Wait for the process to terminate
fi
kubectl port-forward svc/airflow-webserver $PORT:$PORT -n airflow