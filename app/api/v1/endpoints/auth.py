from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.auth import Token
from app.crud.user import user as user_crud

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    user = await user_crud.authenticate(
        db=db, email=form_data.username, password=form_data.password
    )
    token = create_access_token(user.email)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password!",
        )
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user!")

    return {"access_token": token, "token_type": "bearer"}
