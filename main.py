from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['POST']) # Agar tool root URL par hit kar raha hai
def home():
    # 1. API Key Check
    api_key = request.headers.get('x-api-key')
    expected_key = os.getenv("API_KEY")
    
    if api_key != expected_key:
        return jsonify({"error": "Unauthorized"}), 401

    # 2. Body Check (Sabse important fix)
    data = request.get_json(silent=True) # silent=True se error nahi aayega agar body empty ho
    
    if data is None:
        # Tester tool empty body bhej raha ho sakta hai, isliye hum empty dict maan lenge
        data = {}

    return jsonify({
        "status": "success",
        "message": "Honeypot is active",
        "received_data": data
    }), 200

if __name__ == "__main__":
    # Render ke liye port set karna zaroori hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # API Key check karna
    provided_key = request.headers.get('x-api-key')
    actual_key = os.getenv("API_KEY")

    if provided_key != actual_key:
        return jsonify({"error": "Unauthorized"}), 401

    # Request Body handle karna
    # force=True isliye taaki agar header miss ho toh bhi JSON read ho jaye
    data = request.get_json(force=True, silent=True) or {}

    return jsonify({
        "status": "success",
        "message": "Honeypot is active and secured!",
        "received_data": data
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
