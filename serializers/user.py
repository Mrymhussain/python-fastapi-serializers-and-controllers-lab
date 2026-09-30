from pydantic import BaseModel


# Form Validations
class UserRegistrationSchema(BaseModel):
    username: str
    email: str
    password: str


class UserLoginSchema(BaseModel):
    username: str
    password: str


# Response Schemas
class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True


class UserTokenSchema(BaseModel):
    token: str
    message: str