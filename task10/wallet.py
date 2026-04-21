from ecdsa import SigningKey, SECP256k1


class Wallet:
    def __init__(self):
        self.private_key = SigningKey.generate(curve=SECP256k1)
        self.public_key  = self.private_key.get_verifying_key()

    @property
    def address(self) -> str:
        raw = self.public_key.to_string().hex()
        return "0x" + raw[:8] + "..." + raw[-4:]

    def sign(self, data: str) -> str:
        return self.private_key.sign(data.encode()).hex()

    def verify(self, data: str, signature: str) -> bool:
        try:
            return self.public_key.verify(bytes.fromhex(signature), data.encode())
        except Exception:
            return False
