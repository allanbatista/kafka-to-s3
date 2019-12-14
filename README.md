# kafka-to-s3

Cria a capacidade de ler de mais de um tópico do kafka e cria um buffer dos dados coletados em apenas um arquivo .jsonl.

## envs

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_BUCKET_NAME
AWS_PREFIX

KAFKA_TOPIC_NAMES=topic1,topic2
KAFKA_BOOTSTRAP_SERVERS
KAFKA_GROUP_ID
MAX_BUFFER_SIZE=128
MAX_BUFFER_TIME=1
```

## Example

```
sudo docker run -d --restart=unless-stopped --name kafka-twitter-to-s3 \
    -e KAFKA_TOPIC_NAMES=tweets-en,tweets-pt \
    -e KAFKA_GROUP_ID=tweets \
    -e AWS_ACCESS_KEY_ID=XXX \
    -e AWS_SECRET_ACCESS_KEY=xxx \
    -e AWS_BUCKET_NAME=allanbatista-infnet \
    -e AWS_PREFIX=tweets \
    -e KAFKA_BOOTSTRAP_SERVERS=kafka1.infnet.in:9092,kafka2.infnet.in:9092,kafka3.infnet.in:9092,kafka4.infnet.in:9092 \
    -e MAX_BUFFER_SIZE=10240 \
    -e MAX_BUFFER_TIME=60 \
    allanbatista/kafka-to-s3:latest
```
