import os
import secrets
from contextlib import asynccontextmanager
from typing import Annotated, Literal
import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, ConfigDict

def connect():
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)

@asynccontextmanager
async def lifespan(app):
    if len(os.environ.get("ENERGIA_ADMIN_TOKEN", "")) < 32:
        raise RuntimeError("Configure ENERGIA_ADMIN_TOKEN com pelo menos 32 caracteres")
    with connect() as db:
        db.execute("CREATE TABLE IF NOT EXISTS academic_records (id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, city TEXT NOT NULL, category TEXT NOT NULL, description TEXT NOT NULL, created_at TIMESTAMPTZ NOT NULL DEFAULT now())")
    yield

app = FastAPI(title="EnergiaHub Central API", version="1.9", lifespan=lifespan)
bearer = HTTPBearer(auto_error=False)

def authorize(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)]):
    expected = os.environ.get("ENERGIA_ADMIN_TOKEN", "")
    if not expected or not credentials or not secrets.compare_digest(credentials.credentials.encode(), expected.encode()):
        raise HTTPException(401, "Não autorizado", headers={"WWW-Authenticate":"Bearer"})

class Record(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    city: str = Field(min_length=1, max_length=100)
    category: Literal["Simulação acadêmica", "Indicador público"]
    description: str = Field(min_length=1, max_length=200)

@app.get("/health")
def health():
    return {"status":"ok","mode":"academic"}

@app.get("/api/v1/records", dependencies=[Depends(authorize)])
def list_records(limit: int = 100, offset: int = 0):
    if not 1 <= limit <= 500 or offset < 0:
        raise HTTPException(422, "Paginação inválida")
    with connect() as db:
        return db.execute("SELECT * FROM academic_records ORDER BY id LIMIT %s OFFSET %s", (limit,offset)).fetchall()

@app.post("/api/v1/records", status_code=201, dependencies=[Depends(authorize)])
def create(record: Record):
    with connect() as db:
        return db.execute("INSERT INTO academic_records(city,category,description) VALUES (%s,%s,%s) RETURNING *", (record.city,record.category,record.description)).fetchone()

@app.delete("/api/v1/records/{record_id}", dependencies=[Depends(authorize)])
def delete(record_id: int):
    with connect() as db:
        if not db.execute("DELETE FROM academic_records WHERE id=%s", (record_id,)).rowcount:
            raise HTTPException(404,"Registro não encontrado")
        return {"deleted":True}
