import socket
import os
import sys
from concurrent.futures import ThreadPoolExecutor

class Colors:
    RESET = '\033[0m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    ORANGE = '\033[38;5;208m'
    DARKGREEN = '\x1b[32m'
    RED= '\033[31m'

def initServer(SERVER_HOST, SERVER_PORT, timeout):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST,SERVER_PORT))

    server_socket.settimeout(timeout)
    server_socket.listen(5)
    return server_socket

def handle_requests(client_connection, client_address, cwd):
    with client_connection:
        request = client_connection.recv(1024).decode()
        if not request:
            return

        headers = request.split('\n')
        print(f"{Colors.YELLOW}Request from {Colors.ORANGE}{client_address[0]}:{client_address[1]} {Colors.YELLOW} for: {Colors.ORANGE}{headers[0]}{Colors.RESET}")

        try:
            filename = headers[0].split()[1]

            if filename == '/':
                filename = '/index.html'
        
            with open(os.path.join(cwd, 'htdocs') + filename, 'rb') as fin:
                content = fin.read()

            status_line = 'HTTP/1.0 200 OK\r\n\r\n'
            response = status_line.encode() + content
            
        except (IndexError, FileNotFoundError):
            with open(os.path.join(cwd, 'htdocs') + '/404.html', 'rb') as fin:
                content = fin.read()
            status_line = 'HTTP/1.0 404 NOT Found\r\n\r\n'
            response = status_line.encode() + content
    
        client_connection.sendall(response)
        print(f"{Colors.GREEN}Successfully gave response: {Colors.DARKGREEN}{status_line.strip()}{Colors.RESET}\n")

def serve_clients(server_socket, cwd, max_workers):
    with ThreadPoolExecutor(max_workers) as executor:
        while True:
            try:
                client_connection, client_address = server_socket.accept()
                executor.submit(handle_requests, client_connection, client_address, cwd)
            except socket.timeout:
                continue
            except KeyboardInterrupt:
                break
            except Exception as err:
                print(f"{Colors.RED}Server Error: {err}{Colors.RESET}")
        
def main():
    cwd = os.path.dirname(os.path.abspath(sys.argv[0]))

    SERVER_HOST='0.0.0.0'
    SERVER_PORT=8000
    timeout = 1.0
    max_workers = 10

    server_socket = initServer(SERVER_HOST,SERVER_PORT, timeout)
    print(f"{Colors.ORANGE}Listening on port " f"{Colors.GREEN}{SERVER_PORT}\n{Colors.RESET}")

    try:
        serve_clients(server_socket, cwd, max_workers)

    except KeyboardInterrupt:
        pass

    finally:
        print(f"{Colors.ORANGE}--- Server Shutting Down ---{Colors.RESET}")
        server_socket.close()
        print(f"{Colors.YELLOW}Port {Colors.GREEN}{SERVER_PORT}{Colors.YELLOW} is now released.{Colors.RESET}")

if __name__ == "__main__":
    main()