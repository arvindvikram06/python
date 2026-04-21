import hashlib
import json
import time



def merkle_root(transactions: list) -> str:
    if not transactions:
        return "0" * 64
    hashes = [
        hashlib.sha256(json.dumps(tx.to_dict(), sort_keys=True).encode()).hexdigest()
        for tx in transactions
    ]
    while len(hashes) > 1:
        if len(hashes) % 2 != 0:
            hashes.append(hashes[-1])
        hashes = [
            hashlib.sha256((hashes[i] + hashes[i + 1]).encode()).hexdigest()
            for i in range(0, len(hashes), 2)
        ]
    return hashes[0]



class Block:
    def __init__(
        self,
        index: int,
        transactions: list,
        prev_hash: str,
        miner_address: str,
        difficulty: int = 4,
    ):
        self.index         = index
        self.transactions  = transactions
        self.prev_hash     = prev_hash
        self.miner_address = miner_address
        self.difficulty    = difficulty
        self.merkle_root   = merkle_root(transactions)
        self.timestamp     = time.time()
        self.nonce         = 0
        self.hash          = self._mine()


    def _compute_hash(self) -> str:
        data = json.dumps(
            {
                "index":       self.index,
                "merkle_root": self.merkle_root,
                "prev_hash":   self.prev_hash,
                "timestamp":   self.timestamp,
                "nonce":       self.nonce,
            },
            sort_keys=True,
        )
        return hashlib.sha256(data.encode()).hexdigest()

    def _mine(self) -> str:
        target = "0" * self.difficulty
        print(f"       Difficulty: {self.difficulty} (hash must start with '{target}')")
        while True:
            h = self._compute_hash()
            if self.nonce % 10_000 == 0 and self.nonce > 0:
                print(f"       Nonce: {self.nonce:>8,}  -> hash: {h[:8]}...  MISS")
            if h.startswith(target):
                print(f"       Nonce: {self.nonce:>8,}  -> hash: {h[:8]}...  FOUND!")
                return h
            self.nonce += 1

    def to_dict(self) -> dict:
        return {
            "index":        self.index,
            "hash":         self.hash,
            "prev_hash":    self.prev_hash,
            "merkle_root":  self.merkle_root,
            "nonce":        self.nonce,
            "timestamp":    self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "miner":        self.miner_address,
        }

    @classmethod
    def shell_from_dict(cls, data: dict) -> "Block":
        """Reconstruct a lightweight block (no re-mining) for chain validation."""
        b               = cls.__new__(cls)
        b.index         = data["index"]
        b.hash          = data["hash"]
        b.prev_hash     = data["prev_hash"]
        b.merkle_root   = data["merkle_root"]
        b.nonce         = data["nonce"]
        b.timestamp     = data["timestamp"]
        b.transactions  = []
        b.miner_address = data["miner"]
        b.difficulty    = 0          # validated externally
        return b
