from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import mysql.connector
import urllib.request

connection = mysql.connector.connect(
    host="localhost",
    user="mrana23",
    password="Jairam1923",
    database="Project1"
)
cursor = connection.cursor()

class Service2Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Make a request to Microservice 1
        with urllib.request.urlopen('http://localhost:8001/') as response:
            data = response.read().decode('utf-8')
            self.wfile.write(data.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Service2Handler, port=8002):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting Service 2...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
