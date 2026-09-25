import socket

def send_request(sock, method, path, host=True):
    # build the HTTP request string
    req = f"{method} {path} HTTP/1.1\r\n"
    if host:
        req += "Host: localhost\r\n"
    req += "\r\n"
    sock.sendall(req.encode('utf-8'))

def get_response(sock):
    # read exactly one HTTP response
    resp = b""
    while b"\r\n\r\n" not in resp:
        chunk = sock.recv(1024)
        if not chunk:
            print("Server closed connection early!")
            break
        resp += chunk
        
    parts = resp.split(b"\r\n\r\n", 1)
    headers = parts[0].decode('utf-8').split("\r\n")
    
    # find content length
    length = 0
    for h in headers:
        if h.lower().startswith("content-length:"):
            length = int(h.split(":")[1].strip())
            
    body = parts[1]
    # keep reading if we don't have the full body yet
    while len(body) < length:
        body += sock.recv(1024)
        
    status = headers[0]
    return status, body.decode('utf-8')

print("Starting test...")

# 1 socket, 6 responses!
s = socket.create_connection(("localhost", 8080))
print("Connected to server!")

tests = [
    ("GET", "/add?a=2&b=3", True),
    ("GET", "/sub?a=10&b=4", True),
    ("GET", "/mul?a=6&b=7", True),
    ("GET", "/div?a=1&b=0", True),
    ("GET", "/pow?a=2&b=8", True),
    ("POST", "/add", True),
    ("GET", "/add", False) # no host
]

for method, path, use_host in tests:
    print(f"\nSending {method} {path}...")
    send_request(s, method, path, host=use_host)
    status, body = get_response(s)
    print(f"Status: {status}")
    print(f"Result: {body}")

print("\nAll tests finished. Socket is still open? Let's check.")
try:
    # if we send something and it doesn't crash, it's open
    send_request(s, "GET", "/add?a=1&b=1")
    status, body = get_response(s)
    print("Yes! 1 TCP handshake, multiple requests worked.")
except Exception as e:
    print(f"Oops, socket closed: {e}")

s.close()
