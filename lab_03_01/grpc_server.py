import grpc
from concurrent import futures
import message_pb2
import message_pb2_grpc

import random
import string
import json
from langdetect import detect


class MyService(message_pb2_grpc.MyServiceServicer):

    def ProcessLog(self, request, context):
        parts = request.text.split(" ", 2)

        if len(parts) < 3:
            return message_pb2.JsonResponse(json="Invalid log format")

        result = {
            "date": parts[0],
            "level": parts[1],
            "message": parts[2]
        }

        return message_pb2.JsonResponse(json=json.dumps(result))


    def ShortenUrl(self, request, context):
        short = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        return message_pb2.TextResponse(result=f"host.com/{short}")


    def DetectLanguage(self, request, context):
        try:
            lang = detect(request.text)
        except:
            lang = "unknown"

        return message_pb2.TextResponse(result=lang)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    message_pb2_grpc.add_MyServiceServicer_to_server(MyService(), server)
    server.add_insecure_port('[::]:50051')
    print("gRPC сервер запущен на порту 50051...")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()