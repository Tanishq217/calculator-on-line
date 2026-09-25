import socket
import urllib.parse

def handle_client(client_socket, client_address):
    buffer = b""
    while True:
        try:
            # read headers until \r\n\r\n
            while b"\r\n\r\n" not in buffer:
                chunk = client_socket.recv(4096)
                if not chunk:
                    return # client disconnected
                buffer += chunk
                
            header_end = buffer.find(b"\r\n\r\n")
            headers_raw = buffer[:header_end]
            # keep whatever is left in the buffer for the next request!
            buffer = buffer[header_end + 4:]
            
            headers_text = headers_raw.decode('utf-8', errors='replace')
            lines = headers_text.split('\r\n')
            
            if not lines or not lines[0]:
                break
                
            request_line = lines[0]
            parts = request_line.split(" ")
            
            if len(parts) != 3:
                # Malformed request line
                break
                
            method, path_with_query, version = parts
            
            # parse the headers
            headers = {}
            for line in lines[1:]:
                if ":" in line:
                    key, value = line.split(":", 1)
                    headers[key.strip().lower()] = value.strip()
                    
            # Check for Host header as per assignment requirement
            if "host" not in headers and version == "HTTP/1.1":
                resp = f"{version} 400 Bad Request\r\nContent-Length: 0\r\n\r\n"
                client_socket.sendall(resp.encode('utf-8'))
                continue
                
            # If there's a body, we need to consume exactly Content-Length bytes
            content_length = int(headers.get("content-length", 0))
            
            while len(buffer) < content_length:
                chunk = client_socket.recv(4096)
                if not chunk:
                    return
                buffer += chunk
                
            # extract body and leave the rest in buffer for the next pipelined request
            body = buffer[:content_length]
            buffer = buffer[content_length:]
            
            # check method
            if method != "GET":
                resp = f"{version} 405 Method Not Allowed\r\nContent-Length: 0\r\n\r\n"
                client_socket.sendall(resp.encode('utf-8'))
                continue
                
            # routing
            parsed_url = urllib.parse.urlparse(path_with_query)
            path = parsed_url.path
            query = urllib.parse.parse_qs(parsed_url.query)
            
            valid_routes = ['/add', '/sub', '/mul', '/div']
            
            if path not in valid_routes:
                resp = f"{version} 404 Not Found\r\nContent-Length: 0\r\n\r\n"
                client_socket.sendall(resp.encode('utf-8'))
                continue
                
            # extract a and b
            try:
                a = int(query.get('a', [''])[0])
                b = int(query.get('b', [''])[0])
            except (ValueError, IndexError):
                # if missing or not an int
                resp = f"{version} 400 Bad Request\r\nContent-Length: 0\r\n\r\n"
                client_socket.sendall(resp.encode('utf-8'))
                continue
                
            # do math
            result = 0
            if path == '/add':
                result = a + b
            elif path == '/sub':
                result = a - b
            elif path == '/mul':
                result = a * b
            elif path == '/div':
                if b == 0:
                    resp = f"{version} 400 Bad Request\r\nContent-Length: 0\r\n\r\n"
                    client_socket.sendall(resp.encode('utf-8'))
                    continue
                result = int(a / b) # casting to int as per assignment examples
            
            # send back 200 OK
            result_str = str(result)
            resp = f"{version} 200 OK\r\nContent-Length: {len(result_str)}\r\n\r\n{result_str}"
            client_socket.sendall(resp.encode('utf-8'))
            
            # check if connection should be closed
            if headers.get("connection", "").lower() == "close":
                break
                
        except Exception as e:
            print(f"Error with client {client_address}: {e}")
            break
            
    client_socket.close()

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
            
            # handle the client request loop
            handle_client(client_socket, client_address)
            
    except KeyboardInterrupt:
        print("\nShutting down server.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
