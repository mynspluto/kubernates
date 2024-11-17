namenode 실행 됐는데 접속 안됨
Re-format filesystem in Storage Directory root= /var/lib/hadoop-hdfs/cache/hdfs/dfs/name; location= null ? (Y or N) Invalid input:
=> command: ["/bin/bash", "-c"]
args: - |
if [ ! -d "/var/lib/hadoop-hdfs/cache/hdfs/dfs/name/current" ]; then
echo "Y" | hdfs namenode -format
fi
hdfs namenode 로 해결

start-hadoop의 서비스 포트 포워딩 안됨
nohup: 입력 무시
error: unable to forward port because pod is not running. Current status=Pending
=> namenode 켜진 상태에서 다시 kubectl port-forward service/namenode 9870
