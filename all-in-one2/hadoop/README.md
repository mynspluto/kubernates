## 설정, 실행

hadoop/config의 파일들을 임의의 경로에 복사
path: /data/hadoop-config <- 이 부분을 임의의 경로로 변경
minikube mount /data/hadoop-config:/data/hadoop-config로 임의의 경로
미니쿠베에 마운트
./hadoop-restart.sh

## 로그

kubectl logs datanodes-7f467bc4c6-d7nw8

java.io.IOException: Incorrect configuration: namenode address dfs.namenode.servicerpc-address.[] or dfs.namenode.rpc-address.[] is not configured.
at org.apache.hadoop.hdfs.DFSUtil.getNNServiceRpcAddressesForCluster(DFSUtil.java:656)
at org.apache.hadoop.hdfs.server.datanode.BlockPoolManager.refreshNamenodes(BlockPoolManager.java:157)
at org.apache.hadoop.hdfs.server.datanode.DataNode.startDataNode(DataNode.java:1755)
at org.apache.hadoop.hdfs.server.datanode.DataNode.<init>(DataNode.java:564)
at org.apache.hadoop.hdfs.server.datanode.DataNode.makeInstance(DataNode.java:3148)
at org.apache.hadoop.hdfs.server.datanode.DataNode.instantiateDataNode(DataNode.java:3054)
at org.apache.hadoop.hdfs.server.datanode.DataNode.createDataNode(DataNode.java:3098)
at org.apache.hadoop.hdfs.server.datanode.DataNode.secureMain(DataNode.java:3242)
at org.apache.hadoop.hdfs.server.datanode.DataNode.main(DataNode.java:3266)

=> volumeMounts: - name: hadoop-config-volume
mountPath: /opt/hadoop/etc/hadoop
volumes: - name: hadoop-config-volume
configMap:
name: hadoop-config
으로 해결
도커 공식 이미지 레이어를 보니
https://hub.docker.com/layers/apache/hadoop/3.4.1/images/sha256-69ffa97339aff768c4e6120c3fb27aa04c121402b1c8158408a5fb5be586a30e?context=explore
하둡 다운 경로가 /opt/hadoop 이라 /opt/hadoop/etc/hadoop의 컨피그 파일을 교체하면 되었음

org.apache.hadoop.hdfs.server.common.InconsistentFSStateException: Directory /tmp/hadoop-hadoop/dfs/name is in an inconsistent state: storage directory does not exist or is not accessible.
at org.apache.hadoop.hdfs.server.namenode.FSImage.recoverStorageDirs(FSImage.java:392)
at org.apache.hadoop.hdfs.server.namenode.FSImage.recoverTransitionRead(FSImage.java:243)
at org.apache.hadoop.hdfs.server.namenode.FSNamesystem.loadFSImage(FSNamesystem.java:1236)
at org.apache.hadoop.hdfs.server.namenode.FSNamesystem.loadFromDisk(FSNamesystem.java:808)
at org.apache.hadoop.hdfs.server.namenode.NameNode.loadNamesystem(NameNode.java:694)
at org.apache.hadoop.hdfs.server.namenode.NameNode.initialize(NameNode.java:781)
at org.apache.hadoop.hdfs.server.namenode.NameNode.<init>(NameNode.java:1033)
at org.apache.hadoop.hdfs.server.namenode.NameNode.<init>(NameNode.java:1008)
at org.apache.hadoop.hdfs.server.namenode.NameNode.createNameNode(NameNode.java:1782)
at org.apache.hadoop.hdfs.server.namenode.NameNode.main(NameNode.java:1847)
=> hadoop-'hadoop'은 사용한 이미지에서 USER HADOOP 명령어로 user.name을 HADOOP으로 바꿨기 때문에 저 경로에서 찾는것으로 예상
kubernates/hadoop-apache에서 도커 컴포즈로 docker exec ~~ /bin/bash로 확인해본 결과
hadoop-hadoop폴더 존재하는 거 확인
pv, pvc따로 만들어서 마운트하는것으로 해결

리소스매니저 실패
2024-11-16 08:54:40,807 INFO [main] http.HttpServer2 (HttpServer2.java:start(1308)) - HttpServer.start() threw a non Bind IOException
java.net.BindException: Port in use: resourcemanager:8088
at org.apache.hadoop.http.HttpServer2.constructBindException(HttpServer2.java:1369)
at org.apache.hadoop.http.HttpServer2.bindForSinglePort(HttpServer2.java:1391)
at org.apache.hadoop.http.HttpServer2.openListeners(HttpServer2.java:1454)
at org.apache.hadoop.http.HttpServer2.start(HttpServer2.java:1300)
at org.apache.hadoop.yarn.webapp.WebApps$Builder.start(WebApps.java:472)
        at org.apache.hadoop.yarn.server.resourcemanager.ResourceManager.startWepApp(ResourceManager.java:1389)
        at org.apache.hadoop.yarn.server.resourcemanager.ResourceManager.serviceStart(ResourceManager.java:1498)
        at org.apache.hadoop.service.AbstractService.start(AbstractService.java:194)
        at org.apache.hadoop.yarn.server.resourcemanager.ResourceManager.main(ResourceManager.java:1700)
Caused by: java.io.IOException: Failed to bind to resourcemanager/10.110.36.41:8088
        at org.eclipse.jetty.server.ServerConnector.openAcceptChannel(ServerConnector.java:349)
        at org.eclipse.jetty.server.ServerConnector.open(ServerConnector.java:310)
        at org.apache.hadoop.http.HttpServer2.bindListener(HttpServer2.java:1356)
        at org.apache.hadoop.http.HttpServer2.bindForSinglePort(HttpServer2.java:1387)
        ... 7 more
Caused by: java.net.BindException: Cannot assign requested address
        at sun.nio.ch.Net.bind0(Native Method)
        at sun.nio.ch.Net.bind(Net.java:433)
        at sun.nio.ch.Net.bind(Net.java:425)
        at sun.nio.ch.ServerSocketChannelImpl.bind(ServerSocketChannelImpl.java:223)
        at sun.nio.ch.ServerSocketAdaptor.bind(ServerSocketAdaptor.java:74)
        at org.eclipse.jetty.server.ServerConnector.openAcceptChannel(ServerConnector.java:344)
        ... 10 more
2024-11-16 08:54:40,808 INFO  [main] service.AbstractService (AbstractService.java:noteFailure(267)) - Service ResourceManager failed in state STARTED
org.apache.hadoop.yarn.webapp.WebAppException: Error starting http server
        at org.apache.hadoop.yarn.webapp.WebApps$Builder.start(WebApps.java:476)
at org.apache.hadoop.yarn.server.resourcemanager.ResourceManager.startWepApp(ResourceManager.java:1389)
at org.apache.hadoop.yarn.server.resourcemanager.ResourceManager.serviceStart(ResourceManager.java:1498)
at org.apache.hadoop.service.AbstractService.start(AbstractService.java:194)
at org.apache.hadoop.yarn.server.resourcemanager.ResourceManager.main(ResourceManager.java:1700)
Caused by: java.net.BindException: Port in use: resourcemanager:8088
at org.apache.hadoop.http.HttpServer2.constructBindException(HttpServer2.java:1369)
at org.apache.hadoop.http.HttpServer2.bindForSinglePort(HttpServer2.java:1391)
at org.apache.hadoop.http.HttpServer2.openListeners(HttpServer2.java:1454)
at org.apache.hadoop.http.HttpServer2.start(HttpServer2.java:1300)
at org.apache.hadoop.yarn.webapp.WebApps$Builder.start(WebApps.java:472)
        ... 4 more
Caused by: java.io.IOException: Failed to bind to resourcemanager/10.110.36.41:8088
        at org.eclipse.jetty.server.ServerConnector.openAcceptChannel(ServerConnector.java:349)
        at org.eclipse.jetty.server.ServerConnector.open(ServerConnector.java:310)
        at org.apache.hadoop.http.HttpServer2.bindListener(HttpServer2.java:1356)
        at org.apache.hadoop.http.HttpServer2.bindForSinglePort(HttpServer2.java:1387)
        ... 7 more
Caused by: java.net.BindException: Cannot assign requested address
        at sun.nio.ch.Net.bind0(Native Method)
        at sun.nio.ch.Net.bind(Net.java:433)
        at sun.nio.ch.Net.bind(Net.java:425)
        at sun.nio.ch.ServerSocketChannelImpl.bind(ServerSocketChannelImpl.java:223)
        at sun.nio.ch.ServerSocketAdaptor.bind(ServerSocketAdaptor.java:74)
        at org.eclipse.jetty.server.ServerConnector.openAcceptChannel(ServerConnector.java:344)
        ... 10 more
2024-11-16 08:54:40,809 INFO  [main] resourcemanager.ResourceManager (ResourceManager.java:transitionToStandby(1482)) - Transitioning to standby state
2024-11-16 08:54:40,809 INFO  [main] resourcemanager.ResourceManager (ResourceManager.java:transitionToStandby(1489)) - Transitioned to standby state
2024-11-16 08:54:40,809 ERROR [main] resourcemanager.ResourceManager (MarkerIgnoringBase.java:error(159)) - Error starting ResourceManager
org.apache.hadoop.yarn.webapp.WebAppException: Error starting http server
        at org.apache.hadoop.yarn.webapp.WebApps$Builder.start(WebApps.java:476)
at org.apache.hadoop.yarn.server.resourcemanager.ResourceManager.startWepApp(ResourceManager.java:1389)
at org.apache.hadoop.yarn.server.resourcemanager.ResourceManager.serviceStart(ResourceManager.java:1498)
at org.apache.hadoop.service.AbstractService.start(AbstractService.java:194)
at org.apache.hadoop.yarn.server.resourcemanager.ResourceManager.main(ResourceManager.java:1700)
Caused by: java.net.BindException: Port in use: resourcemanager:8088
at org.apache.hadoop.http.HttpServer2.constructBindException(HttpServer2.java:1369)
at org.apache.hadoop.http.HttpServer2.bindForSinglePort(HttpServer2.java:1391)
at org.apache.hadoop.http.HttpServer2.openListeners(HttpServer2.java:1454)
at org.apache.hadoop.http.HttpServer2.start(HttpServer2.java:1300)
at org.apache.hadoop.yarn.webapp.WebApps$Builder.start(WebApps.java:472)
... 4 more
Caused by: java.io.IOException: Failed to bind to resourcemanager/10.110.36.41:8088
at org.eclipse.jetty.server.ServerConnector.openAcceptChannel(ServerConnector.java:349)
at org.eclipse.jetty.server.ServerConnector.open(ServerConnector.java:310)
at org.apache.hadoop.http.HttpServer2.bindListener(HttpServer2.java:1356)
at org.apache.hadoop.http.HttpServer2.bindForSinglePort(HttpServer2.java:1387)
... 7 more
Caused by: java.net.BindException: Cannot assign requested address
at sun.nio.ch.Net.bind0(Native Method)
at sun.nio.ch.Net.bind(Net.java:433)
at sun.nio.ch.Net.bind(Net.java:425)
at sun.nio.ch.ServerSocketChannelImpl.bind(ServerSocketChannelImpl.java:223)
at sun.nio.ch.ServerSocketAdaptor.bind(ServerSocketAdaptor.java:74)
at org.eclipse.jetty.server.ServerConnector.openAcceptChannel(ServerConnector.java:344)
... 10 more
2024-11-16 08:54:40,810 INFO [shutdown-hook-0] resourcemanager.ResourceManager (LogAdapter.java:info(51)) - SHUTDOWN_MSG:
/\***\*\*\*\*\*\*\***\*\*\*\*\***\*\*\*\*\*\*\***\*\*\*\*\***\*\*\*\*\*\*\***\*\*\*\*\***\*\*\*\*\*\*\***
SHUTDOWN_MSG: Shutting down ResourceManager at resourcemanager-6b6fb57bd8-dpkp9/10.244.2.2 \***\*\*\*\*\*\*\***\*\*\*\*\***\*\*\*\*\*\*\***\*\*\*\*\***\*\*\*\*\*\*\***\*\*\*\*\***\*\*\*\*\*\*\***/
=> 카프카 ksqldb가 8088를 쓰고 있기 때문으로 추정했으나
<property>
<name>yarn.resourcemanager.hostname</name>
<value>resourcemanager</value>
</property>
위의 설정때문에
resourcemanager:8088로 실행하고 있었음
<value>0.0.0.0</value>로 수정하여 0.0.0.0:8088로 리소스 매니저 주소 할당하여 실행 성공
