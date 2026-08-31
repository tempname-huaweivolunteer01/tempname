from fastapi import FastAPI

from Routes import CRUD

app = FastAPI()

app.include_router(
        router=CRUD.CRUD_ROUTER,
        prefix="/static_storage",
        tags=["Static Storage Routes"]
        )

@app.get("/")
async def root():
    return{"message": "Default Path"}
