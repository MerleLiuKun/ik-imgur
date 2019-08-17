from tortoise import fields
from tortoise.models import Model

IGNORE_ATTRS = []


class TimestampMixin:
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    modified_at = fields.DatetimeField(null=True, auto_now=True)


class BaseModel(Model):
    # 给予的默认字段
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True
