from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

def aes_encrypt(content: bytes, secret: str='') -> tuple:
    iv = get_random_bytes(16)
    cipher = AES.new(secret.encode('utf-8'), AES.MODE_CFB, iv)
    return iv, cipher.encrypt(content)

def aes_decrypt(content: bytes, secret: str='') -> bytes:
    iv = content[:16]
    cipher = AES.new(secret.encode('utf-8'), AES.MODE_CFB, iv)
    return cipher.decrypt(content[16:])