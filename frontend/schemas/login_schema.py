from pydantic import BaseModel
from typing import List, Optional
from frontend.schemas.user_schema import UserSchema


class LoginSchema(BaseModel):
    user: UserSchema
    token: str