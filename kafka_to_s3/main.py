import os, time, traceback, io, boto3, datetime, uuid
from confluent_kafka import Consumer

aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
aws_bucket_name = os.environ['AWS_BUCKET_NAME']

kafka_topic_name = os.environ['KAFKA_TOPIC_NAME']
kafka_bootstrap_server = os.environ['KAFKA_BOOTSTRAP_SERVERS']
kafka_group_id = os.environ['KAFKA_GROUP_ID']

max_buffer_size = int(os.environ.get('MAX_BUFFER_SIZE') or "128")
max_buffer_time = int(os.environ.get('MAX_BUFFER_TIME') or "1") # seconds

client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)


consumer = Consumer({
    'bootstrap.servers': kafka_bootstrap_server,
    'group.id': kafka_group_id,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
})

consumer.subscribe([kafka_topic_name])


def fetch_messages():
    messages = []
    start = time.time()

    while len(messages) < max_buffer_size and (time.time() - start) < max_buffer_time:
        message = consumer.poll(1)

        if message is None:
            break

        messages.append(message)

    return messages


def build_file(messages):
    file = io.BytesIO()

    for message in messages:
        file.write(message.value() + b"\n")

    file.seek(0)
    return file


def save(file):
    d = datetime.datetime.now().strftime("year=%Y/month=%m/day=%d/hour=%H")
    client.put_object(Bucket=aws_bucket_name, Key=f"{kafka_topic_name}/{d}/{uuid.uuid4()}.jsonl", Body=file)
    return f"s3://{aws_bucket_name}/{kafka_topic_name}/{d}/{uuid.uuid4()}.jsonl"

try:
    while True:
        messages = fetch_messages()

        if messages is not None and len(messages) > 0:
            path = save(build_file(messages))
            print(f"{len(messages)} {path}")
            consumer.commit()
        else:
            print("empty")
            time.sleep(1)

except Exception as e:
    traceback.print_exception(e)
finally:
    consumer.close()
