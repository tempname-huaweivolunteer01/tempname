from fastapi import FastAPI

from app.Routes import CRUD
from app.database.database import Base, engine

app = FastAPI()

app.include_router(
        router=CRUD.CRUD_ROUTER,
        prefix="/books",
        tags=["books"]
        )

@app.get("/")
async def root():
    return{"message": "Default Path"}
