#old discontinued passlib code for hashing etc

# from passlib.context import CryptContext


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# def hash(password: str):
#     return pwd_context.hash(password)

# def verify(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)





#new code for hashing and verifying passwords using pwd library
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

# This replaces your old passlib CryptContext
password_hash = PasswordHash((Argon2Hasher(),))

def hash(password: str):
    return password_hash.hash(password)

def verify(plain_password: str, hashed_password: str):
    return password_hash.verify(plain_password, hashed_password)