from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # 1. API Key Check
    provided_key = request.headers.get('x-api-key')
    actual_key = os.getenv("API_KEY")

    if provided_key != actual_key:
        return jsonify({"error": "Unauthorized"}), 401

    # 2. Body Check (Fix for INVALID_REQUEST_BODY)
    # force=True Flask ko bolega ki content-type sahi na ho toh bhi JSON read kare
    data = request.get_json(force=True, silent=True) or {}

    return jsonify({
        "status": "success",
        "message": "Honeypot is active and secured!",
        "received_data": data
    }), 200

if __name__ == "__main__":
    # Render ke liye port configuration
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
