from pydantic import BaseModel


class CommentSchema(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True


class CreateCommentSchema(BaseModel):
    content: str


class UpdateCommentSchema(BaseModel):
    content: str