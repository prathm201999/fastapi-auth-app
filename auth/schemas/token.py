from pydantic import BaseModel


class Token(BaseModel):
    token_type: str
    refresh_token: str
    access_token: str


class TokenData(BaseModel):
    email: str
