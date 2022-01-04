from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.main import AddressInDB


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
