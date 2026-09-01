from pydantic import BaseModel

class CreateBookSchema(BaseModel):
    name:str
    author:str
    genre:str
    launch_date:str

class EditBookSchema(BaseModel):
    name:str|None = None
    author:str|None = None
    genre:str|None = None
    launch_date:str|None = None
