from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.endpoints import users
from app.db.session import get_db

app = FastAPI(title="Social Media API")

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
