# Calculator on Line

This is my project for the Network Architecture course. It's a simple HTTP/1.1 calculator server built from scratch using only Python sockets.

## Features
- Handles GET requests for math operations: `/add`, `/sub`, `/mul`, `/div`
- Uses query parameters like `?a=10&b=5`
- Keeps the connection open (persistent connection/keep-alive)
- Reads exactly `Content-Length` bytes to handle pipelined requests properly over one socket!

## How to run the server
Just run the python script:
```bash
python server.py
```
The server will start listening on `localhost:8080`.

## How to test it
I also made a `test.py` script to test the keep-alive feature, since we need to make sure the connection stays open for all requests. 
Just run:
```bash
python test.py
```
It will send a bunch of requests over the SAME socket and print the responses to show that it works!
