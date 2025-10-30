from __future__ import annotations
import socket
import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, Event

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

class Server:
    def __init__(self, host="localhost", port=12345, num_allowed_clients=5):
        self.host = host
        self.port = port
        self.logger = logging.getLogger("MainServer")

        # We will use TCP and IPv4 to communicate with clients
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(num_allowed_clients)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(0)

        # Sever Status
        self.running = True
        self.closing = Event()


    def wait_to_get_client_request(self) -> tuple[socket.socket, tuple[str, int]]:
        "Waits for a client to connect"
        return self.server_socket.accept()
    

    def handle_request(self, client_socket, client_address) -> None:
        print(f"Connection from {client_address}")
        
        data = client_socket.recv(2048)
        self.logger.info(f"Received from: {client_address}")

        response_body = "<h1>Hello from the server!</h1>".encode('utf-8')
        response_headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "Connection: close\r\n" # Tell the client you are closing the connection
            "\r\n"
        ).encode('utf-8')

        client_socket.sendall(response_headers)
        client_socket.sendall(response_body)
        client_socket.close()


    def stop(self) -> None:
        self.logger.info(f"Stopping the server")
        self.logger.info(f"Closing all the request threads")

        self.running = False

        self.event_loop_thread.join()
        self.logger.info("Main Event Loop terminated and closed all the request.")

        self.server_socket.close()

        self.logger.info(f"Server successfully stopped")
    

    def run(self) -> None:
        "Run Server"
        self.event_loop_thread = Thread(target=self.server_main_event_loop)
        self.event_loop_thread.start()
        while self.running:
            pass

    def server_main_event_loop(self) -> None:
        client_request = None
        self.logger.info("Server ready to handle requests")
        while self.running:
            try:
                client_request = self.wait_to_get_client_request()
                self.handle_request(*client_request)
            except Exception:
                pass