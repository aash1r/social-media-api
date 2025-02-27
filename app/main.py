from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db

app = FastAPI()

@app.get("/test-db")
async def test_db(db:AsyncSession=Depends(get_db)):
    result = await db.execute(text("SELECT 1"))
    return {"status": "success", "result": result.scalar()}
