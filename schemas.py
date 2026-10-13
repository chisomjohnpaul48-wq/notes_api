from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteUpdate(BaseModel):
    title: str | None = None
    content: str | None = None

class LoginAuth(BaseModel):
    email: str
    password: str