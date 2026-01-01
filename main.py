from fastapi import FastAPI

from routers.roles import router as roles_router

app = FastAPI()


@app.get("/")
def healthcheck():
    return {"status": "ok"}


app.include_router(roles_router)
