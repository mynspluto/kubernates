서로 다른 pod인
namenode와 datanode는 연결되지 않음
서비스, dns 이용해야됨

네임노드, 데이터노드 같이 실행하는법
start-dfs.sh

네임노드, 데이터노드 따로 실행하는법
hdfs namenode, hdfs datanode => 네임노드를 먼져 켜도 데이터노드를 키면 데이터노드가 네임노드에 자동으로 붙는다고 함
