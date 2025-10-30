from __future__ import annotations
import socket, asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


class Server:
    def __init__(self, host="localhost", port=12345):
        self.host = host
        self.port = port
        self.logger = logging.getLogger("MainServer")

        # We will use TCP and IPv4 to communicate with clients
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

        self.executor = None

    def listen(self, num_allowed_clients: int) -> Server:
        self.server_socket.listen(num_allowed_clients)
        self.logger.info(f"Server listening on {self.host}:{self.port}")
        self.executor = ThreadPoolExecutor(max_workers=num_allowed_clients)

        return self
    
    def close(self) -> None:
        self.server_socket.close()
        self.logger.info("Server socket closed")

    def wait_to_get_client_request(self) -> tuple[socket.socket, tuple[str, int]]:
        "Blocking code that waits for a client to connect"
        self.logger.info("Waiting to handle request")
        return self.server_socket.accept()
    
    def handle_request(self) -> None:
        client_connection, client_address = self.wait_to_get_client_request()
        print(f"Connection from {client_address}")
        
        data = client_connection.recv(1024)

        if not data:
            raise Exception

        self.logger.info(f"Received from: {client_address}")

        response_body = "<h1>Hello from the server!</h1>".encode('utf-8')
        response_headers = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(response_body)}\r\n"
            "Connection: close\r\n" # Tell the client you are closing the connection
            "\r\n"
        ).encode('utf-8')

        client_connection.sendall(response_headers)
        client_connection.sendall(response_body)
        client_connection.close()
    
    def run(self) -> None:
        "Main Server Loop that runs"
        running = True
        loop = asyncio.get_event_loop()

        while running:
            try:
                if(len(self.executor._threads) < 1): 
                    loop.run_in_executor(self.executor, self.handle_request)
            except KeyboardInterrupt:
                self.logger.info(f"Server Stopped by the computer user")
                self.logger.info(f"Closing all the request threads")
                
                running = False

        self.logger.info("Server successfully stopped")
        self.server_socket.shutdown(socket.SHUT_RDWR)
        self.server_socket.close()
        self.executor.shutdown(wait=False, cancel_futures=True)
        loop.close()
        self.logger.info(f"Closed all the request")