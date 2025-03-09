from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import get_current_user
from app.crud.user import user as user_crud
from app.db.session import get_db
from app.schemas.user import User, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/", response_model=User)
async def create_user(
    *, db: AsyncSession = Depends(get_db), user_in: UserCreate
) -> User:
    user_exists = await user_crud.get_by_email(db=db, email=user_in.email)
    if user_exists:
        raise HTTPException(
            status_code=400,
            detail=" THe user with this email already exists",
        )
    user = await user_crud.create(db=db, obj_in=user_in)
    return user


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
