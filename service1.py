from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="mrana23",
    password="Jairam1923",
    database="Project1"
)
cursor = connection.cursor()

class Service1Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        response = {'message': 'Hello from Service 1!'}
        self.wfile.write(json.dumps(response).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        user_data = json.loads(post_data.decode('utf-8'))

        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE username = %s", (user_data['username'],))
        user = cursor.fetchone()
        if user:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'User exists'}).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'User not found'}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Service1Handler, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting Service 1...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
