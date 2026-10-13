from exceptions import InvalidCredentialsError
from SQL_queries import create_user, get_user_by_email
from security import hash_password, verify_password, create_access_token
import re


## Email validator
pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
def is_valid_email(email: str):
    return re.match(pattern, email) is not None

def register_user(conn, name, email, password):
    if not name:
        return "Name field must be filled"
    
    if not is_valid_email(email):
        return "Invalid email"
    ##Encrypt password    
    hashed_password = hash_password(password)
    return create_user(conn, name, email, hashed_password)

def login_user(conn, email, password):
    user = get_user_by_email(conn, email)
    if not user:
        raise InvalidCredentialsError()

    if not verify_password(password, user[3]):
        raise InvalidCredentialsError()

    return create_access_token(user[0])