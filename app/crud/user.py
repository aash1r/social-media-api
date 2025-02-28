from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from sqlalchemy import select
from app.schemas.user import UserCreate


class CRUDUser:
    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=obj_in.password,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(self, db: AsyncSession, *, id: int) -> Optional[User]:
        query = select(User).where(User.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()


user = CRUDUser()
