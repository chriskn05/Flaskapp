from flask import Flask, request, jsonify
import hmac
import hashlib
import base64
import time
import requests

app = Flask(__name__)

# API Credentials (replace with your own)
API_KEY = 'bg_a0081bdd9373706e1eae0e383157bc7b'
SECRET_KEY = '8189ded8c1b94d00d49ba1582879bcf4a90e0bdef8db4392e0397dad670d87ce'
BASE_URL = 'https://api.bitget.com'

# Function to generate HMAC signature
def generate_signature(timestamp, method, path, query='', body=''):
    message = f"{timestamp}{method.upper()}{path}{query}{body}"
    mac = hmac.new(
        bytes(SECRET_KEY, encoding='utf-8'),
        bytes(message, encoding='utf-8'),
        hashlib.sha256
    )
    return base64.b64encode(mac.digest()).decode()

# Endpoint to fetch ticker data
@app.route('/bitget/getTicker', methods=['GET'])
def get_ticker():
    # Extract query parameter
    symbol = request.args.get('symbol', 'BTCUSDT')
    timestamp = str(int(time.time() * 1000))
    path = '/api/v2/spot/market/tickers'
    query = f'?symbol={symbol}'
    method = 'GET'

    # Generate signature
    signature = generate_signature(timestamp, method, path, query)

    # Set headers
    headers = {
        'ACCESS-KEY': API_KEY,
        'ACCESS-SIGN': signature,
        'ACCESS-TIMESTAMP': timestamp,
        'Content-Type': 'application/json',
    }

    # Make request to Bitget API
    response = requests.get(f"{BASE_URL}{path}{query}", headers=headers)

    # Return the response as JSON
    return jsonify(response.json())

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
