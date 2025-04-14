from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import BigInteger, JSON
from dotenv import load_dotenv

import os


load_dotenv()

engine = create_async_engine(os.getenv('DB_PATH'))


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    diary: Mapped[list] = mapped_column(JSON)

async def init_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)