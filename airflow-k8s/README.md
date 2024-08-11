kubectl create namespace airflow
kubectl config set-context --current --namespace=airflow
helm uninstall airflow -n airflow
minikube ssh
docker rmi mynspluto-airflow

docker build -t mynspluto-airflow:latest .

minikube image load mynspluto-airflow:latest

helm install airflow apache-airflow/airflow -n airflow -f values.yml

helm upgrade airflow apache-airflow/airflow -n airflow -f values.yml

kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow

id: admin
pw: admin

kubectl exec -it airflow-webserver-948b685fd-5vhbd -- /bin/bash

dag 추가가 안되는 이슈
kubectl exec -it airflow-scheduler-69c669d4f-tt4p5 -- /bin/bash
ls /opt/airflow/dags/
=> 아무것도 안나옴
kubectl describe pod scheduler
=> 만든이미지가 적용 되는게 아니라 dockerhub?의 airflow:2.9.2를 가져다 쓰고 있음
values.yml을 https://airflow.apache.org/docs/helm-chart/stable/parameters-ref.html를 보고 키 값 맞춰서 제대로 작성해야될거 같음
https://airflow.apache.org/docs/apache-airflow-providers-cncf-kubernetes/stable/kubernetes_executor.html도 참고

주가 수집하는 dag 작성
하둡서버 돌리기, 카프카 서버 돌리기
pyspark등으로 하둡에저장, 저장후 카프카 메시지로 저장됐다고 알림
하둡 bash로 접근하여 저장됐는지 확인
카프카 소비자에서 저장됐단 메시지를 받고 하둡에 접근하여 파일 읽어온후 스파크에 올림
데이터 전처리
학습
