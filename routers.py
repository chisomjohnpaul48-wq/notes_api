from fastapi import APIRouter, Depends, HTTPException
from database import get_conn
from exceptions import InvalidCredentialsError
from services import register_user, login_user
from schemas import UserCreate, LoginAuth
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from security import decode_access_token

router = APIRouter()

bearer_scheme = HTTPBearer()
def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    subject = payload.get("sub")
    if subject is None:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    try:
        return int(subject)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")

@router.post("/users", status_code=201)
def create_user_endpoint(user: UserCreate, conn=Depends(get_conn)):
    result = register_user(conn, user.name, user.email, user.password)
    if isinstance(result, str):
        raise HTTPException(status_code=400, detail=result)
    return {"message": "User created successfully", "user_id": result}


@router.post("/auth/login", status_code=200)
def auth_user_endpoint(user: LoginAuth, conn=Depends(get_conn)):
    try:
        result = login_user(conn, user.email, user.password)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid Email or Password.")
    return {
      "access_token": result,
      "token_type": "bearer"
    }


@router.get("/auth/me")
def get_current_user(user_id: int = Depends(get_current_user_id)):
    return {"user_id": user_id}