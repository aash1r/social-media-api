from pydantic import BaseModel, EmailStr

from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str
    role: UserRole


class UpdateUser(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str | None = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    role: UserRole

    class Config:
        from_attributes = True


class User(UserInDB):
    pass
