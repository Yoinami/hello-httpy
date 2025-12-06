from __future__ import annotations
import socket
import logging
from concurrent.futures import ThreadPoolExecutor
from .model.http import Request, Response
from multiprocessing import Process, cpu_count, Pool
import traceback


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

class HelloHttpy:
    def __init__(self, host: str = "localhost", port: int = 12345, num_allowed_clients: int =5):
        self.host = host
        self.port = port
        self.logger = logging.getLogger("MainServer")
        self.num_allowed_clients = num_allowed_clients

        # We will use TCP and IPv4 to communicate with clients
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(self.num_allowed_clients)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(0)

        # Sever Status
        self.running = True


    def wait_to_get_client_request(self) -> tuple[socket.socket, str]:
        "Waits for a client to connect"
        return self.server_socket.accept()
    

    def handle_request(self, client_socket: socket.socket, client_address) -> None:
        print(f"Connection from {client_address}")
        error = False

        try:
        
            byte_data = client_socket.recv(4096)
            self.logger.info(f"Received from: {client_address}")
            
            req: Request = Request.createRequestFromByteString(byte_data)
            self.logger.info(f"{req}")

        except Exception as e:
            print(traceback.format_exc())
            error = True

        response_body = "<h1>Hello from the server!</h1>".encode('utf-8')
        response_headers = (
                f"HTTP/1.1 {200 if not error else 500} OK\r\n"
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
        self.logger.info("Main Event Loop terminated and closed all the request.")

        self.server_socket.close()

        self.logger.info(f"Server successfully stopped")
    

    def run(self) -> None:
        "Run Server"
        self.server_main_event_loop()


    def server_main_event_loop(self) -> None:
        self.logger.info("Server ready to handle requests at: " + str(self.port))

        with ThreadPoolExecutor(max_workers=self.num_allowed_clients) as executor:
            while self.running:
                try:
                    client_socket, client_address = self.wait_to_get_client_request()
                    executor.submit(self.handle_request, client_socket, client_address)
                except IOError:
                    pass
                except Exception as e:
                    print(f"error: {e}")