from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.api.deps import check_permissions, get_current_user
from app.crud.user import user as user_crud
from app.db.session import get_db
from app.models.user import UserRole
from app.schemas.user import User, UserCreate, UpdateUser
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/create", response_model=User)
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


@router.get("/", response_model=List[User])
async def get_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(check_permissions(UserRole.ADMIN)),
):
    return await user_crud.get_all_users(db=db)


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_update: UpdateUser,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(check_permissions(UserRole.ADMIN)),
):
    user = await user_crud.get_by_id(db=db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return await user_crud.update(db, user, user_update)


@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UpdateUser,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Update own user data.
    """
    return await user_crud.update(db, current_user, user_update)
