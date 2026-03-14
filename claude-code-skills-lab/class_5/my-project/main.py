
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Field, create_engine, Session, select
from dotenv import load_dotenv
from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher

password_hash = PasswordHash((Argon2Hasher(),))


def hash_password(password: str) -> str:
    """Hash a password with Argon2."""
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return password_hash.verify(plain_password, hashed_password)


load_dotenv()

engine = create_engine(os.getenv("DB_URL"), echo=True)

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    email: str
    password: str

# Migration Command
# SQLModel.metadata.create_all(engine)


# How to actually interact with tables?

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

# Create User
@app.post("/users")
def create_user(user: User, session: Session = Depends(get_session)):
    if session.exec(select(User).where(User.email == User.email)).first():
        raise HTTPException(status_code=400, detail="User already exists")
    user.password = hash_password(user.password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User created successfully"}

# How to create Table?

def create_tables():
    print("Trying to create table")
    SQLModel.metadata.create_all(engine)
    print("Table Function Completed")
    
create_tables()