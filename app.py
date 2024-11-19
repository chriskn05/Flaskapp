from flask import Flask, request, jsonify
import hmac
import time
import requests
import hashlib
import base64

app = Flask(__name__)

# Replace these with your API credentials
API_KEY = 'bg_a0081bdd9373706e1eae0e383157bc7b'
SECRET_KEY = '8189ded8c1b94d00d49ba1582879bcf4a90e0bdef8db4392e0397dad670d87ce'
PASSPHRASE = '0287fzlhwhjf987293748'
BASE_URL = "https://api.bitget.com"

# Global cache dictionary
cache = {}

# Function to generate HMAC signature
def generate_signature(timestamp, method, path, query='', body=''):
    message = f"{timestamp}{method.upper()}{path}{query}{body}"
    mac = hmac.new(
        bytes(SECRET_KEY, encoding='utf-8'),
        bytes(message, encoding='utf-8'),
        hashlib.sha256
    )
    return base64.b64encode(mac.digest()).decode()

# Endpoint for fetching ticker data
@app.route('/bitget/getTicker', methods=['GET'])
def get_ticker():
    # Get symbol parameter or default to BTCUSDT
    symbol = request.args.get('symbol', 'BTCUSDT')
    
    # Serve from cache if response is less than 5 minutes old
    if symbol in cache and (time.time() - cache[symbol]['timestamp'] < 300):
        return jsonify(cache[symbol]['data'])
    
    # Generate timestamp and signature
    timestamp = str(int(time.time() * 1000))
    query = f"?symbol={symbol}"
    path = "/api/v2/spot/market/tickers"
    signature = generate_signature(timestamp, 'GET', path, query)

    # Set headers
    headers = {
        'ACCESS-KEY': API_KEY,
        'ACCESS-SIGN': signature,
        'ACCESS-TIMESTAMP': timestamp,
        'ACCESS-PASSPHRASE': PASSPHRASE
    }

    # Make the request to Bitget API
    response = requests.get(f"{BASE_URL}{path}{query}", headers=headers)
    data = response.json()
    
    # Cache the response
    cache[symbol] = {'timestamp': time.time(), 'data': data}
    
    return jsonify(data)

# Health check endpoint to test if the app is live
@app.route('/ping', methods=['GET'])
def ping():
    return "pong", 200

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
