from flask import Flask, jsonify, request

from matrices import parse_matrix

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response


@app.route('/matrices/health', methods=['GET'])
def health():
    return jsonify({
        'statut': 'ok',
        'service': 'Service 1 - Calculs Matriciels',
        'port': 5001
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)
