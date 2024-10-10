minikube start --cpus 6 --memory 24000 --driver=docker
minikube addons enable metrics-server
minikube docker-env
eval $(minikube -p minikube docker-env)
unset DOCKER_HOST