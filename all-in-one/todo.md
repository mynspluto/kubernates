1. start, stop, restart sh 작성

2. dag t1, t2, t3 작성
   airflow dag t1(producer) t2(consumer)
   producer에서 consumer에게 신호 보냄
   consumer는 신호를 받고 하둡을 통해 주가 데이터 다운로드
   t1 => t2 데이터 전처리하여 하둡에 업로드 => t3 하둡에서 전처리된 데이터 다운 후 머신러닝
