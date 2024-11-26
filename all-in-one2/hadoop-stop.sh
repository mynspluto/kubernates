kubectl delete all --all -n hadoop
kubectl delete pvc --all -n hadoop
kubectl delete pv --all -n hadoop
#docker system prune -a