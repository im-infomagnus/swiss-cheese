from flask import Flask, request
import requests
import logging

app = Flask(__name__)

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
# Mapping of allowed service names to URLs for safe SSRF avoidance
ALLOWED_URLS = {
    'github': 'https://api.github.com/events',
    'example': 'https://example.com',
}

@app.route('/follow')
def follow_url():
    service = request.args.get('service', '')
    if service in ALLOWED_URLS:
        target_url = ALLOWED_URLS[service]
        try:
            response = requests.get(target_url)
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error performing request to {target_url}: {e}", exc_info=True)
            return "Failed to call the service.", 502
    else:
        return "Invalid or missing service parameter.", 400

@app.route('/')
def home():
    return '''<h1>SSRF</h1>
                <br>
                Usage: When the app is running, use a supported service code to initiate a server-side request:
                    <br><code>http://127.0.0.1:5000/follow?service=github</code><br>
                <br>Available services: github, example<br>
                Running: Navigate to the directory containing ssrf.py and run:
                <br><code>
                    python3 ssrf.py
                </code></br>
    '''

if __name__ == '__main__':
    app.run(debug=True)
