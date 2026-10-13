import jwt
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def hash_password(password):
    hashed_password = password_hash.hash(password)
    return hashed_password

def verify_password(password, hashed_password):
    verified = password_hash.verify(password, hashed_password)
    return verified

load_dotenv()

jwt_secret_key = os.getenv("JWT_SECRET_KEY")
if not jwt_secret_key:
    raise RuntimeError("jwt_secret_key not set.")

def create_access_token(user_id):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=15)
    }
    return jwt.encode(payload, jwt_secret_key, algorithm="HS256")

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        return None