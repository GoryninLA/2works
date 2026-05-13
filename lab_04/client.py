import requests
from cryptography.fernet import Fernet

# Загрузка ключа
with open("encryption_key.txt", "rb") as f:
    key = f.read()

cipher = Fernet(key)

message = input("Введите сообщение: ")

role = input("Введите роль (admin/user): ")

action = input("Введите действие (read/write/delete): ")

encrypted_message = cipher.encrypt(message.encode()).decode()

payload = {
    "message": encrypted_message,
    "role": role,
    "action": action
}

response = requests.post(
    "http://localhost:8000/request",
    json=payload
)

data = response.json()

if data["status"] == "success":

    encrypted_response = data["response"].encode()

    decrypted_response = cipher.decrypt(encrypted_response).decode()

    print(decrypted_response)

else:
    print("\nОшибка:")
    print(data["message"])