from flask import Flask, request, jsonify
import time
import hmac
import hashlib
import os

# Your API Key and Secret Key
API_KEY = "bg_a0081bdd9373706e1eae0e383157bc7b"  # Your provided API Key
SECRET_KEY = "8189ded8c1b94d00d49ba1582879bcf4a90e0bdef8db4392e0397dad670d87ce"

app = Flask(__name__)

@app.route("/generate-signature", methods=["POST"])
def generate_signature():
    data = request.get_json()

    if not data or "method" not in data or "path" not in data:
        return jsonify({"error": "Invalid request payload"}), 400

    method = data["method"].upper()
    path = data["path"]
    body = data.get("body", "")

    # Create the timestamp
    timestamp = str(int(time.time() * 1000))

    # Create the prehash string
    prehash = f"{timestamp}{method}{path}{body}"

    # Generate the HMAC signature
    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        prehash.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    # Return the signature, timestamp, and API key
    return jsonify({
        "api_key": API_KEY,
        "signature": signature,
        "timestamp": timestamp
    })

if __name__ == "__main__":
    # Use the PORT environment variable provided by Render or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
