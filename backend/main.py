from contextlib import closing
import sqlite3
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
app = FastAPI(title="EnergiaHub Demo API", version="1.0.0")
DB = "demo.sqlite3"
def connect():
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute("CREATE TABLE IF NOT EXISTS records (id INTEGER PRIMARY KEY, city TEXT, category TEXT, description TEXT)")
    return db
class Record(BaseModel):
    city: str = Field(min_length=1, max_length=100)
    category: Literal["Simulação acadêmica", "Indicador público"]
    description: str = Field(min_length=1, max_length=200)
@app.get("/health")
def health():
    return {"status":"ok","mode":"demo"}
@app.get("/api/v1/records")
def list_records():
    with closing(connect()) as db:
        return [dict(r) for r in db.execute("SELECT * FROM records ORDER BY id")]
@app.post("/api/v1/records", status_code=201)
def create(record: Record):
    with closing(connect()) as db, db:
        cur = db.execute("INSERT INTO records(city,category,description) VALUES (?,?,?)",(record.city,record.category,record.description))
        return {"id":cur.lastrowid,**record.model_dump()}
@app.delete("/api/v1/records/{record_id}")
def delete(record_id: int):
    with closing(connect()) as db, db:
        cur = db.execute("DELETE FROM records WHERE id=?",(record_id,))
        if not cur.rowcount:
            raise HTTPException(404,"Registro não encontrado")
        return {"deleted":True}
