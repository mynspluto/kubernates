# 베이스 이미지로부터 시작
FROM mysql:latest

# 환경 변수 설정 (루트 비밀번호, 데이터베이스 이름, 사용자 이름, 사용자 비밀번호)
ENV MYSQL_ROOT_PASSWORD=dbslzhs90!
ENV MYSQL_DATABASE=kubernetes_express
ENV MYSQL_AUTHENTICATION_PLUGIN=mysql_native_password

RUN rm -rf /var/lib/mysql
# init.sql 파일과 init.sh 파일을 컨테이너 내부로 복사하여 MySQL이 실행될 때 자동으로 실행되도록 함
COPY ./init.sql /docker-entrypoint-initdb.d/