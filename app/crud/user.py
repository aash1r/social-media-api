import app
import app.core
import app.core.security
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, List, Optional, Union, Any
from sqlalchemy import select
from app.schemas.user import UserCreate, UpdateUser
from app.core.security import get_password_hash, verify_password


class CRUDUser:
    async def create(self, db: AsyncSession, *, obj_in: UserCreate) -> User:

        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            role=obj_in.role,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def authenticate(self, db: AsyncSession, *, email: str, password: str):
        user = await self.get_by_email(db=db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        query = select(User).where(User.email == email)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id(self, db: AsyncSession, *, id: int) -> Optional[User]:
        query = select(User).where(User.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_users(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[User]:
        query = select(User).offset(skip).limit(limit)
        result = await db.execute(query)
        print(result)
        return result.scalars().all()

    async def update(
        self, db: AsyncSession, db_obj: User, obj_in: Union[UpdateUser, Dict[str, Any]]
    ):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if update_data.get("password"):
            hashed_password = get_password_hash(update_data["password"])
            update_data["password"] = hashed_password
            # del update_data["password"]

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


user = CRUDUser()
