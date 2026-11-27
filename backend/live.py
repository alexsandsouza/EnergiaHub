"""Collaborative reports, not verified electricity status."""
import os
import secrets
from contextlib import asynccontextmanager
from typing import Literal
import psycopg
from psycopg.rows import dict_row
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, ConfigDict, Field

def connect():
    return psycopg.connect(os.environ["DATABASE_URL"], row_factory=dict_row)

@asynccontextmanager
async def lifespan(app):
    if len(os.environ.get("ENERGIA_REPORT_TOKEN", "")) < 32:
        raise RuntimeError("Configure ENERGIA_REPORT_TOKEN (32+ caracteres)")
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS community_reports (
            id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            city TEXT NOT NULL, neighborhood TEXT NOT NULL,
            kind TEXT NOT NULL CHECK (kind IN ('falta','retorno')),
            created_at TIMESTAMPTZ NOT NULL DEFAULT now())""")
        db.execute("CREATE INDEX IF NOT EXISTS community_reports_created_idx ON community_reports(created_at)")
    yield

app = FastAPI(title="EnergiaHub Live API", version="3.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["https://alexsandsouza.github.io"], allow_methods=["GET"], allow_headers=[])
bearer = HTTPBearer(auto_error=False)

def authorize(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    expected = os.environ.get("ENERGIA_REPORT_TOKEN", "")
    if not expected or not credentials or not secrets.compare_digest(credentials.credentials.encode(), expected.encode()):
        raise HTTPException(401, "Não autorizado")

class Report(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    city: str = Field(min_length=2,max_length=100,pattern=r"^[^0-9@/]+$")
    neighborhood: str = Field(min_length=2,max_length=100,pattern=r"^[^0-9@/]+$")
    kind: Literal["falta","retorno"]

@app.get("/health")
def health():
    with connect() as db:
        db.execute("SELECT 1")
    return {"status":"ok","mode":"community_unverified"}

@app.post("/api/v1/reports",status_code=201,dependencies=[Depends(authorize)])
def report(body: Report):
    with connect() as db:
        db.execute("INSERT INTO community_reports(city,neighborhood,kind) VALUES (%s,%s,%s)",(body.city.casefold(),body.neighborhood.casefold(),body.kind))
    return {"accepted":True,"verified":False}

@app.get("/api/v1/summary")
def summary():
    # Publish only statewide totals from completed daily buckets, not live outage locations.
    with connect() as db:
        rows=db.execute("""SELECT (created_at AT TIME ZONE 'America/Manaus')::date AS day,
          count(*) AS reports FROM community_reports
          WHERE created_at >= now() - interval '30 days'
          AND (created_at AT TIME ZONE 'America/Manaus')::date < (now() AT TIME ZONE 'America/Manaus')::date
          GROUP BY 1 HAVING count(*) >= 5 ORDER BY 1 DESC""").fetchall()
    return {"scope":"Amazonas","verified":False,"meaning":"Volume de relatos, não situação de fornecimento","data":rows}
