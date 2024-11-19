from flask import Flask, request, jsonify
import time
import hmac
import hashlib
import os

app = Flask(__name__)

# Your API Key and Secret Key
API_KEY = "bg_a0081bdd9373706e1eae0e383157bc7b"
SECRET_KEY = "8189ded8c1b94d00d49ba1582879bcf4a90e0bdef8db4392e0397dad670d87ce"

@app.route("/generate-signature", methods=["POST"])
def generate_signature():
    # Parse the JSON payload from the request
    data = request.get_json()

    # Validate the required fields in the request
    if not data or "method" not in data or "path" not in data:
        return jsonify({"error": "Invalid request payload"}), 400

    # Extract request details
    method = data["method"].upper()
    path = data["path"]
    body = data.get("body", "")

    # Generate a timestamp
    timestamp = str(int(time.time() * 1000))

    # Construct the prehash string
    prehash = f"{timestamp}{method}{path}{body}"

    # Create HMAC signature
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        prehash.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    # Return the signature, timestamp, and API key in JSON format
    return jsonify({
        "api_key": API_KEY,
        "signature": signature,
        "timestamp": timestamp
    })

if __name__ == "__main__":
    # Support dynamic port binding for deployment
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
