from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
import ssl
import sys

app = Flask(__name__)

PORT = int(sys.argv[1])

# Загрузка ключа шифрования
with open("encryption_key.txt", "rb") as f:
    key = f.read()

cipher = Fernet(key)

# RBAC
ROLE_PERMISSIONS = {
    "admin": ["read", "write", "delete"],
    "user": ["read"]
}


@app.route("/process", methods=["POST"])
def process_data():
    try:
        data = request.json

        encrypted_message = data["message"].encode()
        role = data["role"]
        action = data["action"]

        # Проверка прав доступа
        if action not in ROLE_PERMISSIONS.get(role, []):
            return jsonify({
                "status": "error",
                "message": f"Access denied for role '{role}'"
            }), 403

        # Расшифровка сообщения
        decrypted_message = cipher.decrypt(encrypted_message).decode()

        print(f"[SERVER {PORT}] Получено сообщение: {decrypted_message}")

        # Приведение к нижнему регистру
        message_lower = decrypted_message.lower()

        # Логика ответов сервера
        if "привет" in message_lower:
            response_text = (
                f"Ответ сервера на порту {PORT}: "
                f"Привет! Как дела?"
            )

        elif "как дела" in message_lower:
            response_text = (
                f"Ответ сервера на порту {PORT}: "
                f"У меня всё отлично 😄 А у тебя?"
            )

        elif "пока" in message_lower:
            response_text = (
                f"Ответ сервера на порту {PORT}: "
                f"Пока! Хорошего дня 👋"
            )

        elif "кто ты" in message_lower:
            response_text = (
                f"Ответ сервера на порту {PORT}: "
                f"Я защищённый сервер распределённой системы"
            )

        elif "сервер" in message_lower:
            response_text = (
                f"Ответ сервера на порту {PORT}: "
                f"Сейчас запрос обработал сервер {PORT}"
            )

        else:
            response_text = (
                f"Ответ сервера на порту {PORT}: "
                f"получено сообщение '{decrypted_message}'"
            )

        # Шифрование ответа
        encrypted_response = cipher.encrypt(
            response_text.encode()
        ).decode()

        return jsonify({
            "status": "success",
            "response": encrypted_response
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":

    # HTTPS SSL context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    context.load_cert_chain(
        certfile="certificates/server_cert.pem",
        keyfile="certificates/server_key.pem"
    )

    app.run(
        host="0.0.0.0",
        port=PORT,
        ssl_context=context
    )