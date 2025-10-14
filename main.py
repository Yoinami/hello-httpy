import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "localhost"
port = 12345
server_socket.bind((host, port))

server_socket.listen(5)
print(f"Server listening on {host}:{port}")

while True:
    client_connection, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    client_connection.sendall(b"Welcome to Server")

    try:
        while True:
            data = client_connection.recv(1024)

            if not data:
                break

            print(f"Reveived from {client_address}: {data.decode()}")
            client_connection.sendall(data)
    finally:
        client_connection.close()
        print(f"Connection with {client_address} closed")