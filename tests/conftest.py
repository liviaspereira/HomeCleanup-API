import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app, get_session


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="create_address")
def create_address_fixture():
    return {
        "street_name": "Conde",
        "street_number": 123456,
        "city": "Extrema",
        "postal_code": "18958-875",
        "country": "Brasil",
        "user_id": 1,
        "size": 69,
        "number_of_rooms": 3,
    }

@pytest.fixture(name="create_user")
def create_user_fixture():
    return {
    "name": "Lucas",
    "email": "lucaschato@chato.com",
    "phone": "658555226",
    "password": "askjhahjsa055",
    "is_home_owner": True,
    }