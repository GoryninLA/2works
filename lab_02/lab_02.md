# Лабораторная работа №2
**Тема:** Разработка REST API и настройка обратного прокси Nginx  
**Группа:** ЦИБ-241
**Дата:** 17.03.2026  

---

## 1. Цель работы
Цель работы: изучить принципы HTTP, REST API и работу обратного прокси Nginx, реализовать API для "Личных заметок" с кэшированием и проверить цепочку редиректов.

---

## 2. Краткие теоретические сведения
- **HTTP** — протокол передачи гипертекста, работает по принципу запрос-ответ. Коды состояния: 200 OK, 301 Moved Permanently, 403 Forbidden и др.  
- **REST API** — архитектурный стиль взаимодействия клиента и сервера через HTTP. Основные методы: GET, POST, PUT, DELETE.  
- **Nginx** — веб-сервер и обратный прокси, может проксировать запросы к внутренним серверам, управлять кэшем, редиректами и балансировкой нагрузки.

---

## 3. Номер и описание варианта задания
**Вариант: 4**

**Лабораторная работа №2**

**Задание:**
1. Проверка цепочки редиректов с http://mail.ru → https://mail.ru  
2. Реализация API для "Личных заметок" (сущность: id, title, content)  
3. Настройка кэширования GET-запросов на 1 минуту  

---
## Архитектура инструментов PEST API с Nginx


## 4. Ход выполнения

### Часть 1. Проверка цепочки редиректов с http://mail.ru → https://mail.ru
**Команда:**

```bash
curl -v http://mail.ru
```

**Первый ответ:**
```bash
HTTP/1.1 301 Moved Permanently
Location: https://mail.ru/
```
Значение:
- сервер говорит: “иди на HTTPS”
- это постоянный редирект (301)
- Вывод: сайт принудительно переводит на защищённое соединение

**Второй ответ:**
```bash
HTTP/2 302
Location: https://login.vk.ru/...
```
Значение:
- временный редирект (302)
- тебя отправляют на авторизацию через VK
- Вывод: используется внешняя система авторизации

**Третий ответ:**
```bash
HTTP/2 302
Location: https://account.mail.ru/login?...
```
Значение:
- возвращают обратно на Mail
- но теперь на страницу логина

**Последний ответ:** 
```bash
HTTP/2 200
```
Значение:
- страница загрузилась успешно
- редиректы закончились

### Часть 2. Реализация API для "Личных заметок" (сущность: id, title, content)
## Установка Flask 
```python
pip install Flask
```
<img width="640" height="408" alt="Снимок экрана 2026-03-18 в 11 00 10" src="https://github.com/user-attachments/assets/8bad8856-fdd1-40e4-bdbd-1c4b3df13f7b" />

## Листинг кода app.py
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

notes = []
current_id = 1


@app.route('/api/notes', methods=['GET'])
def get_notes():
    return jsonify(notes)


@app.route('/api/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    for note in notes:
        if note['id'] == note_id:
            return jsonify(note)
    return jsonify({"error": "Not found"}), 404


@app.route('/api/notes', methods=['POST'])
def create_note():
    global current_id
    data = request.get_json()

    note = {
        "id": current_id,
        "title": data.get("title"),
        "content": data.get("content")
    }

    notes.append(note)
    current_id += 1

    return jsonify(note), 201


if __name__ == '__main__':
    app.run(port=5050)
```
Комментарии:
- GET /api/notes — возвращает все заметки
- GET /api/notes/<id> — возвращает конкретную заметку
- POST /api/notes — добавляет новую заметку

## Листинг конфигурации Nginx (измененные части)
```bash
http {
    include       mime.types;
    default_type  application/octet-stream;

    proxy_cache_path /tmp/nginx_cache levels=1:2 keys_zone=my_cache:10m max_size=100m inactive=1m use_temp_path=off;

    server {
        listen       8080;
        server_name  localhost;

        location / {
            root   html;
            index  index.html index.htm;
        }

        location /api/ {
            proxy_pass http://127.0.0.1:5050;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_cache my_cache;
            proxy_cache_valid 200 1m;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}
```

## Результаты тестирования
- Получение данных (GET)
```bash
curl http://localhost:8080/api/notes | jq
```
<img width="443" height="530" alt="Снимок экрана 2026-03-18 в 11 09 42" src="https://github.com/user-attachments/assets/316975ef-9454-4b92-b5a3-a27e46a7c08b" />

- Добавление данных (POST)
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"title":"Test4","content":"Hello4"}' \
http://localhost:8080/api/notes
```
<img width="369" height="86" alt="Снимок экрана 2026-03-18 в 11 19 15" src="https://github.com/user-attachments/assets/23f93d3f-9464-49bf-88cc-1e81683b828b" />

## Вывод
В ходе лабораторной работы я проверил работу HTTP и редиректов, реализовал REST API для "Личных заметок" на Flask, настроил Nginx как обратный прокси для API, добавил кэширование GET-запросов на 1 минуту , убедился, что API работает через Nginx и напрямую через Flask.

