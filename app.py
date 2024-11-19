from flask import Flask, request, jsonify
import time
import hmac
import hashlib

app = Flask(__name__)

# Replace these with your actual API credentials
API_KEY = "bg_a0081bdd9373706e1eae0e383157bc7b"
SECRET_KEY = "8189ded8c1b94d00d49ba1582879bcf4a90e0bdef8db4392e0397dad670d87ce"

@app.route('/generate-signature', methods=['POST'])
def generate_signature():
    data = request.json  # Get JSON data from the POST request
    method = data.get("method")  # HTTP method (GET, POST, etc.)
    path = data.get("path")      # Endpoint path (e.g., /markets/ticker)
    body = data.get("body", "")  # Request body (optional)

    # Generate timestamp (current time in milliseconds)
    timestamp = str(int(time.time() * 1000))

    # Create the pre-hash string
    pre_hash_string = f"{timestamp}{method}{path}{body}"

    # Generate HMAC-SHA256 signature
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        pre_hash_string.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()

    # Return the API key, signature, and timestamp as a JSON response
    return jsonify({
        "api_key": API_KEY,
        "signature": signature,
        "timestamp": timestamp
    })

if __name__ == '__main__':
    app.run(port=5000)  # Run the app on port 5000
