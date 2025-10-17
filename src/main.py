import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "localhost"
port = 12345
server_socket.bind((host, port))

server_socket.listen(5)
print(f"Server listening on {host}:{port}")
running = True

while running:
    client_connection, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    try:
        while running:
            try:
                data = client_connection.recv(1024)

                if not data:
                    break

                print(f"""=======================\nReveived from {client_address}\n======================== \n{data.decode()}\n======================""")

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
            except KeyboardInterrupt:
                running = False

    except ConnectionAbortedError:
        print(f"Connection closed by client: {client_address}")
    except KeyboardInterrupt:
        print(f"Server Stopped by the computer user")
        break
    finally:
        client_connection.close()
        print(f"Connection with {client_address} closed")