from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import mysql.connector

# Establish a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="mrana23",
    password="Jairam1923",
    database="Project1"
)
cursor = connection.cursor()

class HealthRecordsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        # Retrieve health records from the database
        cursor.execute("SELECT * FROM health_records")
        records = cursor.fetchall()
        self.wfile.write(json.dumps(records).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=HealthRecordsHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting server...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
