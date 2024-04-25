# Node.js 버전 14를 기반으로 하는 이미지를 사용
FROM node:14

# 앱 디렉토리 생성
WORKDIR /usr/src/app

# 앱 의존성 설치
COPY package*.json ./
RUN npm install

# 앱 소스 추가
COPY . .

# 앱 실행
CMD [ "npm", "run", "start" ]