from passlib.context import CryptContext
pswd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pswd_context.hash(password)