from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(settings.database_url,echo=True)
async_session = sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession,None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e
        


