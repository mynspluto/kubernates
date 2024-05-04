#!/bin/bash
set -e

# MySQL 데이터 디렉토리 초기화
mysqld --initialize-insecure --basedir=var/lib/mysql --datadir=/ --console

# 다른 초기화 작업 수행
# 필요한 경우 이곳에 추가적인 초기화 작업을 수행할 수 있습니다.
