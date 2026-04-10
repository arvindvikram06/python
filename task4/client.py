import socket, json
from config import *

s = socket.socket()
s.connect((SOCKET_HOST, SOCKET_PORT))

task = {
    "func": "send_email",
    "args": ["arvind@co.com", "welcome"]
}

s.send(json.dumps(task).encode())
print(s.recv(1024).decode())
s.close()