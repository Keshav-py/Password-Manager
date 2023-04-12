import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def create_key(password):

    password = password.encode()
    salt = b'\xb6\xea\x0e\xffGd\x03\xb2\x95\xc1\x8b\xcb\x8c\x1bVm'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))

    return key


def encrypt_file(key):

    f = Fernet(key)
    with open("passes.csv", "rb+") as passes_csv:
        passes = passes_csv.read()

    encrypted = f.encrypt(passes)

    with open("passes.csv", "wb") as passes_csv:
        passes_csv.write(encrypted)


def decrypt_file(key):
    f = Fernet(key)
    with open("passes.csv", "rb+") as passes_csv:
        passes = passes_csv.read()

    decrypted = f.decrypt(passes)

    with open("passes.csv", "wb") as passes_csv:
        passes_csv.write(decrypted)

    return decrypted.decode()





