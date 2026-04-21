import time
from wallet import Wallet


class Transaction:
    def __init__(self, sender_wallet: Wallet, recipient_address: str, amount: float):
        self.sender        = sender_wallet.address
        self.recipient     = recipient_address
        self.amount        = amount
        self.timestamp     = time.time()
        self._data_str     = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}"
        self.signature     = sender_wallet.sign(self._data_str)
        self._wallet       = sender_wallet

    def is_valid(self) -> bool:
        return self._wallet.verify(self._data_str, self.signature)

    def to_dict(self) -> dict:
        return {
            "sender":    self.sender,
            "recipient": self.recipient,
            "amount":    self.amount,
            "timestamp": self.timestamp,
            "signature": self.signature[:20] + "...",
        }
