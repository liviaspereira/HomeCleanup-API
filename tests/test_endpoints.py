from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import AddressInDB, UserInDB


def test_create_address_no_body(client):
    response = client.post("/address/")
    assert response.status_code == 400


def test_create_address_bad_body(client):
    response = client.post("/address/", json={"Erro": "erro"})
    assert response.status_code == 422


@pytest.mark.freeze_time("2017-05-21")
def test_create_address(create_address, session: Session, client: TestClient):
    response = client.post("/address/", json=create_address)
    assert response.status_code == 201

    address = session.get(AddressInDB, 1)
    expected_data = create_address
    expected_data["id"] = 1
    expected_data["is_active"] = True
    expected_data["created_at"] = datetime.now()
    assert address.dict() == expected_data


def test_delete_address_not_found(client):
    response = client.delete("/address/1")
    assert response.status_code == 404


def test_delete_address(create_address, session: Session, client: TestClient):
    address_in_db = AddressInDB(**create_address, created_at=datetime.now())
    session.add(address_in_db)
    session.commit()

    response = client.delete("/address/1")
    assert response.status_code == 204

    address_from_db = session.get(AddressInDB, 1)
    assert address_from_db is None

def test_delete_id_no_exist(create_address, session: Session, client: TestClient):
    address_in_db = AddressInDB(**create_address, created_at=datetime.now())
    session.add(address_in_db)
    session.commit()
    response = client.delete("/address/5")
    assert response.status_code == 404

    address_from_db = session.get(AddressInDB, 1)
    assert address_from_db is not None

def test_create_user_no_body(client):
    response = client.post("/users/")
    assert response.status_code == 400

def test_create_user_bad_body(client):
    response = client.post("/users/", json={"Erro": "erro"})
    assert response.status_code == 422

@pytest.mark.freeze_time("2017-05-21")
def test_create_user(client, session, create_user):
    response = client.post("/users/", json=create_user)
    assert response.status_code == 201

    user = session.get(UserInDB, 1)
    expected_data = create_user
    expected_data["id"] = 1
    expected_data["is_active"] = True
    expected_data["created_at"] = datetime.now()
    del expected_data["password"]
    del user.hashed_password
    assert user.dict() == expected_data








