import hashlib
from base64 import b64encode
from uuid import uuid4

ALGORITHM = "sha256"
ITERATIONS = 100000


def generate_salt(length: int = 12) -> str:
    assert 0 <= length <= 32, "Salt length must be between 0 and 32"

    uuid = uuid4()
    hash = hashlib.sha256(uuid.bytes).digest()
    salt = hash[:length]
    return b64encode(salt).decode("ascii")


def generate_hash(password: str, salt: str) -> str:
    hash = hashlib.pbkdf2_hmac(
        hash_name=ALGORITHM,
        password=password.encode("ascii"),
        salt=salt.encode("ascii"),
        iterations=ITERATIONS,
    )
    return b64encode(hash).decode("ascii")
