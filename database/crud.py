from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm.attributes import flag_modified

from datetime import datetime

from database.init_db import User, engine


async_session = async_sessionmaker(bind=engine)


async def add_user(tg_id: int):
    async with async_session() as session:
        user = await session.get(User, tg_id)
        if user is None:
            user = User(tg_id=tg_id)
            session.add(user)
            await session.commit()

async def add_food(tg_id: int, calories: int):
    async with async_session() as session:
        user = await session.get(User, tg_id)
        
        today = datetime.now().strftime('%Y-%m-%d')
        if user.diary is None:
            user.diary = {}
        
        if today in user.diary:
            user.diary[today] += calories
            flag_modified(user, 'diary')
        else:
            user.diary[today] = calories

        await session.commit()
