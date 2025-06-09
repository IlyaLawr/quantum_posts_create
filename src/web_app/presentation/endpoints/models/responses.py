from pydantic import BaseModel


class CreateResponse(BaseModel):
    id: int
    message: str


class UpdateResponse(BaseModel):
    success: bool
    message: str


class DeleteResponse(BaseModel):
    success: bool
    message: str
