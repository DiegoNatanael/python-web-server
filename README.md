# 🌐 Simple Python Web Server

*A bare-bones HTTP server built from scratch in Python, demonstrating fundamental web server principles, static file serving, and concurrency.*

<br>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

<br>

## 📖 About The Project

This project implements a rudimentary HTTP 1.1 web server capable of serving static files (HTML, CSS, etc.) from a designated 'public' directory. Built entirely from scratch using Python's `socket` module, it aims to demystify how web servers operate at a low level, handling requests, responses, and file serving.

It showcases core networking concepts and introduces multithreading to manage multiple simultaneous client connections efficiently. This project is ideal for understanding the mechanics behind more complex web frameworks.

## ✨ Key Features

* **HTTP GET Support:** Processes basic HTTP GET requests.
* **Static File Serving:** Delivers HTML, CSS, and other files from a configurable `public` directory.
* **Basic Routing:** Serves `index.html` by default for the root path (`/`).
* **Concurrency:** Utilizes Python's `threading` module to handle multiple client connections concurrently, preventing the server from blocking on a single request.
* **Graceful Shutdown:** Implements `Ctrl+C` (KeyboardInterrupt) handling for a clean server shutdown.
* **Error Handling:** Provides 404 Not Found, 405 Method Not Allowed, and 500 Internal Server Error responses.

## 🚀 How It Works

The server operates on a classic client-server model:

1.  **Socket Creation & Binding:** A TCP/IP socket is created and bound to a specified host (localhost) and port.
2.  **Listening for Connections:** The server continuously listens for incoming client connections.
3.  **Connection Acceptance:** When a client connects, the server accepts the connection.
4.  **Thread Spawning:** A new thread is immediately spawned to handle the accepted client connection. This allows the main server thread to return to listening for new clients, ensuring concurrency.
5.  **Request Parsing:** The client handler thread reads the HTTP request, parses the method (only GET is supported) and the requested path.
6.  **File Retrieval:** It maps the requested path to a file within the `public` directory.
7.  **Response Generation:** It constructs an HTTP response, including appropriate headers (Content-Type, Content-Length) and the file's content (or an error page).
8.  **Response Sending & Connection Closure:** The response is sent back to the client, and the connection is closed.

## 🛠️ Built With

* **Python 3.x:** Core programming language.
* **Standard Library:** Primarily `socket`, `os`, `mimetypes`, and `threading` modules.

## 🏁 Getting Started

To get a local copy of the web server running:

### Prerequisites

* Python 3.x installed on your system.

### Installation

1.  Clone this repository to your local machine:
    ```sh
    git clone [https://github.com/](https://github.com/)[YOUR_GITHUB_USERNAME]/simple-python-web-server.git
    ```
2.  Navigate into the project directory:
    ```sh
    cd simple-python-web-server
    ```
3.  Ensure you have a `public` directory in the same location as `simple_server.py`, containing at least `index.html`.

### Usage

1.  Run the server from your terminal:
    ```sh
    python simple_server.py
    ```
2.  Open your web browser and navigate to `http://127.0.0.1:8080` (or the port specified in `simple_server.py`, e.g., 8888).
3.  You should see the `index.html` page. Try accessing other files like `http://127.0.0.1:8080/about.html` if you have them.
4.  To stop the server, press `Ctrl+C` in your terminal.


## 📬 Contact

Project Link: [https://github.com/DiegoNatanael/simple-python-web-server](https://github.com/DiegoNatanael/simple-python-web-server)
