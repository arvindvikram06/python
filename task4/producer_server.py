import socket, json, uuid, time
from queue_manager import push_task
from config import *

def create_task(func, args):
    return {
        "id": str(uuid.uuid4())[:6],
        "func": func,
        "args": args,
        "status": "PENDING",
        "retries": 0,
        "start_time": None,
        "end_time": None
    }

server = socket.socket()
server.bind((SOCKET_HOST, SOCKET_PORT))
server.listen(5)

print("[PRODUCER] Listening...")

while True:
    client, _ = server.accept()
    data = client.recv(1024).decode()

    req = json.loads(data)
    task = create_task(req["func"], req["args"])

    push_task(task)

    client.send(f"Task queued {task['id']}".encode())
    client.close()