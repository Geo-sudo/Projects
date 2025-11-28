import socket
import os
import sys
from concurrent.futures import ThreadPoolExecutor

class Colors:
    RESET = '\033[0m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ORANGE = '\033[38;5;208m'

def initServer(SERVER_HOST, SERVER_PORT, timeout):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST,SERVER_PORT))

    server_socket.settimeout(timeout)
    server_socket.listen(1)
    return server_socket

def serve(server_socket, run_path):
    while True:
        try:
            client_connection, client_address = server_socket.accept()
        except:
            continue
        
        request = client_connection.recv(1024).decode()
        headers = request.split('\n')
        print(f"{Colors.YELLOW}Request from {Colors.ORANGE}{client_address[0]}:{client_address[1]} {Colors.YELLOW} for: {Colors.ORANGE}{headers[0]}{Colors.RESET}")

        try:
            filename = headers[0].split()[1]

            if filename == '/':
                filename = '/index.html'
        
            fin = open(run_path + filename)
            content = fin.read()
            fin.close()

            response = 'HTTP/1.0 200 OK\n\n' + content
            
        except:
            fin = open(run_path + '/404.html')
            content = fin.read()
            fin.close()
            response = 'HTTP/1.0 404 NOT Found\n\n' + content
    
        client_connection.sendall(response.encode())
        client_connection.close()
        print(f"{Colors.GREEN}\nSuccessfully gave response! \n{Colors.RESET}")

def main():
    cwd = os.path.dirname(os.path.abspath(sys.argv[0]))
    run_path = os.path.join(cwd, 'htdocs')

    SERVER_HOST='0.0.0.0'
    SERVER_PORT=8000
    timeout = 1.0

    server_socket = initServer(SERVER_HOST,SERVER_PORT, timeout)
    print(f"{Colors.ORANGE}Listening on port " f"{Colors.YELLOW}{SERVER_PORT}\n{Colors.RESET}")

    try:
        serve(server_socket, run_path)

    except KeyboardInterrupt:
        pass

    finally:
        print(f"\n{Colors.ORANGE}--- Server Shutting Down Gracefully ---{Colors.RESET}")
        server_socket.close()
        print(f"{Colors.YELLOW}Port {SERVER_PORT} is now released.{Colors.RESET}")

if __name__ == "__main__":
    main()