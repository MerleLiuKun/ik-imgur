from tortoise import Tortoise

from config import DB_URL


# 初始化数据库
async def init_db(create_db=False):
    await Tortoise.init(
        db_url=DB_URL,
        modules={'models': ['app.models']},
        _create_db=create_db
    )
