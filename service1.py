# Name      : Mattrey Kumar Rana
# Email     : mrana23@myseneca.ca
# Date      : 3/7/2024


from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import hashlib
import mysql.connector

# Establish a connection to the MySQL database
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

        # Retrieve user's medical history from the database
        cursor.execute("SELECT * FROM medical_history WHERE user_id = %s", (self.user_id,))
        records = cursor.fetchall()
        self.wfile.write(json.dumps(records).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        user_data = json.loads(post_data.decode('utf-8'))

        if 'action' in user_data and user_data['action'] == 'register':
            # Register a new user
            username = user_data['username']
            password = user_data['password']

            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Check if user already exists
            cursor.execute("SELECT * FROM user WHERE username = %s", (username,))
            existing_user = cursor.fetchone()
            if existing_user:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'User already exists'}).encode('utf-8'))
                return

            # Insert new user into the database
            cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, hashed_password))
            user_id = cursor.lastrowid
            connection.commit()

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'message': 'User registered successfully'}).encode('utf-8'))
        else:
            # Authenticate user
            username = user_data['username']
            password = user_data['password']

            # Hash the password
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            # Check if user exists and password matches
            cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, hashed_password))
            user = cursor.fetchone()
            if user:
                self.user_id = user[0]  # Store the user_id for later use
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'User authenticated'}).encode('utf-8'))
            else:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Authentication failed'}).encode('utf-8'))

    def do_PUT(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        medical_history_data = json.loads(post_data.decode('utf-8'))

        # Insert medical history record for the user
        cursor.execute("INSERT INTO medical_history (user_id, record_type, record_data) VALUES (%s, %s, %s)",
                       (self.user_id, medical_history_data['record_type'], medical_history_data['record_data']))
        connection.commit()

        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': 'Medical history added successfully'}).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=Service1Handler, port=8001):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting Service 1...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
