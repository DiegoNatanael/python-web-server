import socket
import os
import mimetypes
import threading
import time

# Configuration
HOST = '127.0.0.1'
PORT = 8080 
DOC_ROOT = 'public' 

# Ensure the public directory exists
if not os.path.isdir(DOC_ROOT):
    print(f"Error: Document root '{DOC_ROOT}' not found.")
    print("Please create a folder named 'public' in the same directory as this script.")
    exit()

# Helper function to parse the HTTP request line
def parse_request_line(request_line):
    parts = request_line.split(' ')
    if len(parts) == 3:
        method, path, _ = parts
        return method, path
    return None, None

# Helper function to get the MIME type for a file
def get_mime_type(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type is None:
        return 'application/octet-stream' 
    return mime_type

# Function to handle each client connection in a separate thread
def handle_client(conn, addr):
    try:
        request_data = conn.recv(1024).decode('utf-8')
        if not request_data:
            return 

        request_lines = request_data.split('\r\n')
        first_line = request_lines[0]
        method, request_path = parse_request_line(first_line)

        print(f"\n[{threading.current_thread().name}] --- Request from {addr} ---")
        print(f"[{threading.current_thread().name}] Method: {method}, Path: {request_path}")
        print(f"[{threading.current_thread().name}] ------------------------")

        if method == 'GET':
            if request_path == '/':
                file_to_serve = os.path.join(DOC_ROOT, 'index.html')
            else:
                file_to_serve = os.path.join(DOC_ROOT, request_path.lstrip('/'))

            if os.path.exists(file_to_serve) and os.path.isfile(file_to_serve):
                with open(file_to_serve, 'rb') as f:
                    response_body = f.read()

                mime_type = get_mime_type(file_to_serve)

                response_headers = [
                    "HTTP/1.1 200 OK",
                    f"Content-Type: {mime_type}",
                    f"Content-Length: {len(response_body)}",
                    "Connection: close",
                    "\r\n"
                ]
                response = "\r\n".join(response_headers).encode('utf-8') + response_body
                conn.sendall(response)
                print(f"[{threading.current_thread().name}] [{addr}] Served file: {file_to_serve}")
            else:
                response_body = b"<h1>404 Not Found</h1><p>The requested resource was not found on this server.</p>"
                response_headers = [
                    "HTTP/1.1 404 Not Found",
                    "Content-Type: text/html",
                    f"Content-Length: {len(response_body)}",
                    "Connection: close",
                    "\r\n"
                ]
                response = "\r\n".join(response_headers).encode('utf-8') + response_body
                conn.sendall(response)
                print(f"[{threading.current_thread().name}] [{addr}] 404 Not Found: {request_path}")
        else:
            response_body = b"<h1>405 Method Not Allowed</h1><p>Only GET requests are supported.</p>"
            response_headers = [
                "HTTP/1.1 405 Method Not Allowed",
                "Content-Type: text/html",
                f"Content-Length: {len(response_body)}",
                "Connection: close",
                "\r\n"
            ]
            response = "\r\n".join(response_headers).encode('utf-8') + response_body
            conn.sendall(response)
            print(f"[{threading.current_thread().name}] [{addr}] 405 Method Not Allowed: {method} {request_path}")

    except Exception as e:
        print(f"[{threading.current_thread().name}] [{addr}] Error handling client: {e}")
        error_body = b"<h1>500 Internal Server Error</h1><p>Something went wrong on the server.</p>"
        error_headers = [
            "HTTP/1.1 500 Internal Server Error",
            "Content-Type: text/html",
            f"Content-Length: {len(error_body)}",
            "Connection: close",
            "\r\n"
        ]
        error_response = "\r\n".join(error_headers).encode('utf-8') + error_body
        conn.sendall(error_response)
    finally:
        conn.close()
        print(f"[{threading.current_thread().name}] [{addr}] Connection closed.")


def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((HOST, PORT))
        print(f"Server listening on http://{HOST}:{PORT}")
    except OSError as e:
        print(f"Error binding socket: {e}")
        print("Perhaps the port is already in use? Try a different port number.")
        return

    server_socket.listen(5)
    print("Main thread: Entering connection acceptance loop...")

    try:
        while True:
            print("Main thread: Waiting for a new connection...")
            conn, addr = server_socket.accept()
            print(f"Main thread: Accepted connection from {addr}. Spawning new thread...")

            # Create and start a new thread for each connection
            client_handler = threading.Thread(target=handle_client, args=(conn, addr))
            client_handler.daemon = True
            client_handler.start()
            print(f"Main thread: Thread {client_handler.name} started for {addr}.")

    except KeyboardInterrupt: 
        print("\nMain thread: KeyboardInterrupt detected. Shutting down server...")
    finally: 
        server_socket.close()
        print("Main thread: Server socket closed.")

if __name__ == "__main__":
    run_server()