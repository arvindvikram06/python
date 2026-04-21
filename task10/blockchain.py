import hashlib
import threading
import time

from block import Block
from transaction import Transaction

MINING_REWARD = 1.0


class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.chain      = [self._genesis()]
        self.mempool    = []
        self._lock      = threading.Lock()


    def _genesis(self) -> Block:
        b               = Block.__new__(Block)
        b.index         = 0
        b.transactions  = []
        b.prev_hash     = "0" * 64
        b.miner_address = "genesis"
        b.difficulty    = 0
        b.merkle_root   = "0" * 64
        b.timestamp     = time.time()
        b.nonce         = 0
        b.hash          = hashlib.sha256(b"genesis").hexdigest()
        return b

    @property
    def last_block(self) -> Block:
        return self.chain[-1]


    def add_transaction(self, tx: Transaction) -> bool:
        if tx.is_valid():
            with self._lock:
                self.mempool.append(tx)
            return True
        return False


    def mine_block(self, miner_address: str) -> Block:
        with self._lock:
            pending      = self.mempool[:]
            self.mempool = []

        print(f"\n=== Mining ===")
        print(f"[NODE] Mining block #{len(self.chain)} ({len(pending)} transactions in mempool)...")

        start = time.time()
        block = Block(len(self.chain), pending, self.last_block.hash, miner_address, self.difficulty)
        elapsed = round(time.time() - start, 2)

        print(f"\n[NODE] Block #{block.index} mined in {elapsed}s")
        print(f"       Hash:         {block.hash[:16]}...")
        print(f"       Prev Hash:    {block.prev_hash[:16]}...")
        print(f"       Merkle Root:  {block.merkle_root[:8]}...")
        print(f"       Transactions: {len(block.transactions)}")
        print(f"       Miner Reward: {MINING_REWARD} coin -> {miner_address}")

        self.chain.append(block)
        return block


    def add_block(self, block: Block) -> bool:
        if block.prev_hash != self.last_block.hash:
            return False
        if not block.hash.startswith("0" * self.difficulty):
            return False
        if block.index != self.last_block.index + 1:
            return False
        self.chain.append(block)
        return True


    def get_balance(self, address: str) -> float:
        balance = 0.0
        for block in self.chain[1:]:
            for tx in block.transactions:
                if tx.sender    == address: balance -= tx.amount
                if tx.recipient == address: balance += tx.amount
            if block.miner_address == address:
                balance += MINING_REWARD
        return round(balance, 4)
