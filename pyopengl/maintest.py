import socket

host = "127.0.0.1"
port = 8080

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host, port))

socket.send(b"Hello, server!")

socket.close()