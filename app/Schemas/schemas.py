from pydantic import BaseModel

class CreateBookSchema(BaseModel):
    name:str
    author:str
    genre:str
    launch_date:str
