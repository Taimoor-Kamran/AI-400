from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

password_hash = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    """Hash a password with Argon2."""
    return password_hash.hash(password)

print(hash_password("taimoor_345"))
print(hash_password("saqlain_345"))
print(hash_password("yousuf_345"))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return password_hash.verify(plain_password, hashed_password)