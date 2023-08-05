# Copyright 2021 iiPython
# Diffie Hellman Algorithm

# Modules
import random
try:
    from Crypto.Cipher import AES
    from Crypto.Hash import SHA256

    no_support = False

except ImportError:
    no_support = True
    pass  # No crypto support

# Hellman class
class Hellman(object):
    def __init__(self, base: int, modu: int) -> None:
        if no_support:
            raise RuntimeError("you need pycryptodome to use this!")

        self.base = base
        self.modu = modu

        self.priv_key = random.randint(1000, 9999)
        self.pub_key = self.generate_public(self.priv_key)

        self.shared_key = None
        self.hash_key = None

    def pad(self, string: str) -> str:
        return string + (16 - len(string) % 16) * "\5"

    def generate_public(self, priv: int) -> int:
        """
        Generates a public key given a private key.
        """
        return (self.base ** priv) % self.modu

    def generate_shared(self, pub: int) -> int:
        """
        Generates a shared secret key given another users public key.
        """
        self.shared_key = (pub ** self.priv_key) % self.modu
        self.hash_key = SHA256.new(str(self.shared_key).encode("utf8")).digest()
        return self.shared_key

    def encrypt(self, data: str) -> bytes:
        if self.shared_key is None:
            raise RuntimeError("no shared key has been established yet!")

        cipher = AES.new(self.hash_key, AES.MODE_ECB)
        return cipher.encrypt(self.pad(data).encode("utf8"))

    def decrypt(self, data: bytes) -> str:
        if self.shared_key is None:
            raise RuntimeError("no shared key has been established yet!")

        decipher = AES.new(self.hash_key, AES.MODE_ECB)
        pt = decipher.decrypt(data).decode("utf8")
        return pt[:pt.find("\5")]
