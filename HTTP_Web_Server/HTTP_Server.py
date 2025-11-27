import socket

class Colors:
    RESET = '\033[0m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ORANGE = '\033[38;5;208m'

SERVER_HOST='0.0.0.0'
SERVER_PORT=8000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST,SERVER_PORT))
server_socket.listen(1)
print(f"{Colors.ORANGE}Listening on port " f"{Colors.YELLOW}{SERVER_PORT}\n{Colors.RESET}")

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    print(request)

    response = 'HTTP/1.0 200 OK\n\n <h1>Hello Web!</h1>'
    client_connection.sendall(response.encode())
    client_connection.close()
    print(f"{Colors.GREEN}\nSuccessfully gave response! \n{Colors.RESET}")


server_socket.close()