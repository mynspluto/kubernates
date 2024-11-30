서로 다른 pod인
namenode와 datanode는 연결되지 않음
서비스, dns 이용해야됨

네임노드, 데이터노드 같은 파드에서 실행하는법

방법 1. start-dfs.sh => 세컨더리 네임노드, 리소스매너저 등도 같이 실행되며 다른 하둡노드도 같이 켜짐, ssh 설정이 필요
방법 2. hdfs namenode & sleep 5 hdfs datanode => ssh 설정 불필요 다른 하둡노드 같이 안켜짐

네임노드, 데이터노드 다른 파드에서 실행하는법
hdfs namenode, hdfs datanode => 네임노드를 먼져 켜도 데이터노드를 키면 데이터노드가 네임노드에 자동으로 붙는다고 함
etc/hosts에서 127.0.0.1 namenode-service 추가하면 해결될 것으로 예상
