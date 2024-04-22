kubectl run nginx-app --image nginx --port=80
kubectl get pods
kubectl expose pod nginx-app --type=NodePort
kubectl get services
kubectl get nodes -o wide
kubectl get ep
minikube service nginx-app
