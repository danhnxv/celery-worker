from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    ordered: Optional[bool] = False


class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)
