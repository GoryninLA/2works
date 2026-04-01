import pika
import grpc
import message_pb2
import message_pb2_grpc
import json

def main():
    # Подключение к RabbitMQ
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', credentials=credentials)
    )
    channel = connection.channel()
    
    # Объявляем очередь
    channel.queue_declare(queue='task_queue', durable=True)
    
    print(' [*] Ожидание сообщений. Для выхода нажмите CTRL+C')
    
    # Создаем gRPC канал и заглушку
    grpc_channel = grpc.insecure_channel('localhost:50051')
    stub = message_pb2_grpc.MyServiceStub(grpc_channel)
    
    def callback(ch, method, properties, body):
        text = body.decode()
        print(f" [x] Получено сообщение: {text}")
        
        try:
            # Автоматически определяем тип сообщения и вызываем соответствующий метод
            if text.startswith("http"):
                # Если сообщение начинается с http - сокращаем URL
                result = stub.ShortenUrl(message_pb2.TextRequest(text=text))
                print(f" [✓] Сокращенный URL: {result.result}")
                
            elif len(text.split()) >= 3:
                # Если в сообщении 3 и более слов - пробуем распарсить как лог
                result = stub.ProcessLog(message_pb2.TextRequest(text=text))
                print(f" [✓] Обработанный лог: {result.json}")
                
            else:
                # Иначе определяем язык
                result = stub.DetectLanguage(message_pb2.TextRequest(text=text))
                print(f" [✓] Определенный язык: {result.result}")
                
        except grpc.RpcError as e:
            print(f" [✗] Ошибка gRPC: {e.details()}")
        except Exception as e:
            print(f" [✗] Ошибка: {str(e)}")
        
        # Подтверждаем обработку сообщения
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    # Обрабатываем только одно сообщение за раз
    channel.basic_qos(prefetch_count=1)
    
    # Начинаем слушать очередь
    channel.basic_consume(queue='task_queue', on_message_callback=callback)
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n [*] Остановка consumer...")
        connection.close()

if __name__ == '__main__':
    main()