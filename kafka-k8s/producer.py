# producer.py
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='kafka.confluent.svc.cluster.local:9071',
    value_serializer=lambda v: str(v).encode('utf-8')
)

for i in range(10):
    producer.send('my-topic', value=f'Hello, Kafka! {i}')
producer.flush()
producer.close()