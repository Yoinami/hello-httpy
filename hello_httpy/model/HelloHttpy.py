from __future__ import annotations
import socket
import logging
from concurrent.futures import ThreadPoolExecutor
from .http import Request, Response
from threading import Thread, Event


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

        # We will use TCP and IPv4 to communicate with clients
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(num_allowed_clients)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setblocking(0)

        # Sever Status
        self.running = True
        self.closing = Event()


    def wait_to_get_client_request(self) -> tuple[socket.socket, str]:
        "Waits for a client to connect"
        return self.server_socket.accept()
    

    def handle_request(self, client_socket: socket.socket, client_address) -> None:
        print(f"Connection from {client_address}")
        
        byte_data = client_socket.recv(2048)
        self.logger.info(f"Received from: {client_address}")
        
        req: Request = Request.createRequestFromByteString(byte_data)
        self.logger.info(f"{req}")

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
            except IOError:
                pass
            except Exception as e:
                print(f"error: {e}")
            finally:
                if client_request:
                    client_request[0].close()