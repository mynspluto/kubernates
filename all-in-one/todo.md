1. start, stop, restart sh 작성

2. 카프카 start.sh stop.sh, t1(producer), t2(consumer): upload to hadoop
   start.kafka.sh 클러스터 주소 가져와서 토픽 생성하는 부분 따로 빼야할듯
   => t1에서 토픽 가져와서 리스트 보고 없으면 생성
   stop.sh후 start.sh하면 confluent-operator-745b699c76-6gj8g만 생성되고 그 뒤로 나머지 파드 생성안됨 다시 stop후 start하면 생성됨 원인 모름 pod지워지는걸 끝까지 안기다려서 그런가?

3. 하둡 start.sh stop.sh t3(download at hadoop)

4. dag t1, t2, t3 작성
   airflow dag t1(producer) t2(consumer)
   producer에서 consumer에게 신호 보냄
   consumer는 신호를 받고 하둡을 통해 주가 데이터 다운로드
   t1 => t2 데이터 전처리하여 하둡에 업로드 => t3 하둡에서 전처리된 데이터 다운 후 머신러닝

hadoop dockerfile amd64 arm64 분기처리

[hadoop 파일 업로드 403 에러]
cd /usr/local/hadoop/bin
hdfs dfs -chmod -R 777 /
