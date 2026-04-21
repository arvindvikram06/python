import json
import socket
import threading

from block import Block
from blockchain import Blockchain
from wallet import Wallet


class Node:
    def __init__(self, node_id: int, port: int, peer_ports: list, difficulty: int = 4):
        self.node_id    = node_id
        self.port       = port
        self.peer_ports = peer_ports
        self.wallet     = Wallet()
        self.blockchain = Blockchain(difficulty=difficulty)
        self._stop      = threading.Event()


    def _log(self, msg: str):
        print(f"[NODE-{self.node_id}] {msg}")


    def broadcast_block(self, block: Block):
        data = json.dumps(block.to_dict()).encode()
        for port in self.peer_ports:
            try:
                with socket.create_connection(("127.0.0.1", port), timeout=2) as s:
                    s.sendall(data)
            except Exception:
                pass 

    

    def _server(self):
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind(("127.0.0.1", self.port))
        srv.listen(5)
        srv.settimeout(1)
        while not self._stop.is_set():
            try:
                conn, _ = srv.accept()
                raw = b""
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    raw += chunk
                conn.close()
                threading.Thread(target=self._handle_block, args=(raw,), daemon=True).start()
            except socket.timeout:
                continue
        srv.close()

    def _handle_block(self, raw: bytes):
        try:
            data  = json.loads(raw.decode())
            block = Block.shell_from_dict(data)

            if block.index <= self.blockchain.last_block.index:
                return  

            accepted = self.blockchain.add_block(block)
            status   = (
                f"Accepted (chain height: {len(self.blockchain.chain) - 1})"
                if accepted else "Rejected"
            )
            self._log(f"Received block #{block.index} validating... {status}")
        except Exception as e:
            self._log(f"Bad block received: {e}")


    def start(self):
        self._log(f"Listening on port {self.port} | Wallet: {self.wallet.address}")
        threading.Thread(target=self._server, daemon=True).start()

    def stop(self):
        self._stop.set()
