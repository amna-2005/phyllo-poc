import json
import urllib.request
import urllib.error
import base64
from http.server import BaseHTTPRequestHandler

CLIENT_ID = '111f2a7d-b14e-4061-95f4-67f44e08aee2'
CLIENT_SECRET = 'ed8cfbb6-965f-46d4-8094-0e802c6eb4a6'
BASE_URL = 'https://api.staging.getphyllo.com'
AUTH = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))
        data = json.dumps({
            'user_id': body.get('user_id'),
            'products': ['IDENTITY']
        }).encode()
        req = urllib.request.Request(BASE_URL + '/v1/sdk-tokens', data=data, method='POST')
        req.add_header('Authorization', 'Basic ' + AUTH)
        req.add_header('Content-Type', 'application/json')
        try:
            with urllib.request.urlopen(req) as res:
                result = res.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(result)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(e.read())
