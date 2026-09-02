from uuid import UUID

from pydantic import BaseModel, ConfigDict

class CreateBookSchema(BaseModel):
    name:str
    author:str
    genre:str
    launch_date:str

class BookResponseSchema(CreateBookSchema):
    id: UUID
    model_config = ConfigDict(from_attributes=True)