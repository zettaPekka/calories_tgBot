from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.init_db import User, engine


async_session = async_sessionmaker(bind=engine)


async def add_user(tg_id: int):
    async with async_session() as session:
        user = await session.get(User, tg_id)
        if user is None:
            user = User(tg_id=tg_id)
            session.add(user)
            await session.commit()
