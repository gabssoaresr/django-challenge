from pydantic import BaseModel
from typing import List, Optional

class UserSchema(BaseModel):
    id: int 
    name: str 
    email: str
    phone: str
    is_active: bool
    is_staff: bool
    is_superuser: bool