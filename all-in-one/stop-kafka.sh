helm uninstall confluent-operator --namespace kafka
kubectl delete -f ./kafka/platform-kraft.yml
kubectl delete all --all -n kafka
# kubectl delete pvc --all -n kafka
# kubectl delete pv --all -n kafka