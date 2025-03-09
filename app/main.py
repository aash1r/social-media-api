from fastapi import FastAPI

from app.api.v1.endpoints import auth, users


app = FastAPI(title="Social Media API")

app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
