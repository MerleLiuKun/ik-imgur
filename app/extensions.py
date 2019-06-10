import sentry_sdk
from sentry_sdk.integrations.sanic import SanicIntegration
from tortoise import Tortoise

import config


# 初始化数据库
async def init_db(create_db=False):
    await Tortoise.init(
        db_url=config.DB_URL,
        modules={'models': ['app.models']},
        _create_db=create_db
    )


sentry_sdk.init(
    dsn=config.SENTRY_DSN,
    integrations=[SanicIntegration()]
)
