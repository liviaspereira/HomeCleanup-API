from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Session, SQLModel, create_engine


class UserCreate(BaseModel): 
    name: str
    email: EmailStr
    phone: str
    password: str
    is_home_owner: bool


class UserInDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone: str
    name: str
    email: str
    hashed_password: str
    is_home_owner: bool
    created_at: datetime
    is_active: Optional[bool] = Field(default=True)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)


@app.post("/users/", status_code=201)
async def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(
        **user.dict(exclude={"password"}),
        hashed_password=hashed_password,
        created_at=datetime.now(),
    )
    with Session(engine) as session:
        session.add(user_in_db)
        session.commit()
    return


def get_password_hash(password):
    return pwd_context.hash(password)