from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db.session import SessionLocal

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def healthcheck():
    return {"status": "ok"}
