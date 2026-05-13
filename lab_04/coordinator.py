from flask import Flask, request, jsonify
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

SERVERS = [
    "https://127.0.0.1:5001/process",
    "https://127.0.0.1:5002/process"
]

CERT = (
    "certificates/client_cert.pem",
    "certificates/client_key.pem"
)


@app.route("/request", methods=["POST"])
def forward_request():

    data = request.json

    for server in SERVERS:

        try:
            response = requests.post(
                server,
                json=data,
                cert=CERT,
                verify=False,
                timeout=3
            )

            return jsonify(response.json())

        except Exception as e:
            print(f"Сервер недоступен: {server}")
            print(e)

    return jsonify({
        "status": "error",
        "message": "Все серверы недоступны"
    }), 500


if __name__ == "__main__":
    app.run(port=8000)