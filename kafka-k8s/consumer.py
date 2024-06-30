# consumer.py
from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'my-topic',
    bootstrap_servers='kafka.confluent.svc.cluster.local:9071',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group'
)

for message in consumer:
    print(f"Received message: {message.value.decode('utf-8')}")
