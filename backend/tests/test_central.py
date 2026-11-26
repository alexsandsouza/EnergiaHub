import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import ValidationError
from backend.central import Record, authorize

def test_valid_record():
    record = Record(city=" Manaus ", category="Indicador público", description="Exemplo acadêmico")
    assert record.city == "Manaus"

@pytest.mark.parametrize("city,category,description", [
    (" ", "Indicador público", "Exemplo"),
    ("Manaus", "Inválida", "Exemplo"),
    ("Manaus", "Indicador público", " "),
])
def test_invalid_record(city, category, description):
    with pytest.raises(ValidationError):
        Record(city=city, category=category, description=description)

def test_authorization(monkeypatch):
    token = "a" * 40
    monkeypatch.setenv("ENERGIA_ADMIN_TOKEN", token)
    authorize(HTTPAuthorizationCredentials(scheme="Bearer", credentials=token))
    for credentials in [None, HTTPAuthorizationCredentials(scheme="Bearer", credentials="wrong")]:
        with pytest.raises(HTTPException) as error:
            authorize(credentials)
        assert error.value.status_code == 401
