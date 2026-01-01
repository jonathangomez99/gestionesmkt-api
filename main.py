from fastapi import FastAPI
from db.session import get_db
from routers import roles

app = FastAPI()

app.include_router(roles.router)

@app.get("/")
def healthcheck():
    return {"status": "ok"}
