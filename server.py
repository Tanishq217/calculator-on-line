import socket

def main():
    # Setting up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # bind to localhost on port 8080
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(5)
    print("Server is listening on port 8080...")

    try:
        while True:
            # accept incoming connections
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")
            
            # just close it for now, will implement handling later
            client_socket.close()
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
