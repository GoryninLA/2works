import pika
import sys

# подключение
credentials = pika.PlainCredentials('user', 'password')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)

channel = connection.channel()

# очередь
channel.queue_declare(queue='task_queue', durable=True)

# сообщение из аргумента
message = ' '.join(sys.argv[1:]) or "Test message"

# отправка
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=2,
    )
)

print(f"[x] Отправлено: {message}")

connection.close()