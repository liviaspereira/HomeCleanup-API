from datetime import datetime
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, Session, SQLModel, create_engine, select


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


class AddressCreate(BaseModel):
    street_name: str
    street_number: int
    city: str
    postal_code: str
    country: str
    user_id: int
    size: int
    number_of_rooms: int


class AddressInDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    country: str
    street_name: str
    street_number: int
    city: str
    postal_code: str
    size: int
    number_of_rooms: int
    created_at: datetime
    is_active: Optional[bool] = Field(default=True)
    user_id: int


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)


@app.post("/users/", status_code=201)
async def create_user(user: UserCreate = None, session: Session = Depends(get_session)):    

    if not user:
        raise HTTPException(status_code=400, detail="Body is required")
    hashed_password = get_password_hash(user.password)
    user_in_db = UserInDB(
        **user.dict(exclude={"password"}),
        hashed_password=hashed_password,
        created_at=datetime.now(),
    )
    session.add(user_in_db)
    session.commit()
    return


def get_password_hash(password):
    return pwd_context.hash(password)


@app.post("/address/", status_code=201)
async def create_address(
    address: AddressCreate = None, session: Session = Depends(get_session)
):
    if not address:
        raise HTTPException(status_code=400, detail="Body is required")
    address_in_db = AddressInDB(
        **address.dict(),
        created_at=datetime.now(),
    )
    session.add(address_in_db)
    session.commit()
    return


@app.delete("/address/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_id: int, session: Session = Depends(get_session)):
    try:
        address = session.exec(
            select(AddressInDB).where(AddressInDB.id == address_id)
        ).one()
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Address not found"
        )
    session.delete(address)
    session.commit()
