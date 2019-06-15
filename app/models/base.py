from tortoise import fields
from tortoise.models import Model
from tortoise.models import ModelMeta as _ModelMeta

IGNORE_ATTRS = []


class PropertyHolder(type):
    """
    定义元类 用于为 Model 的基类补充默认字段
    This follow https://github.com/dongweiming/lyanna/blob/master/models/base.py
    魔鬼, 董大竟然魔改了 Tortoise-ORM 字段初始化的代码
    TODO 此处先用董大版本
    """

    def __new__(mcs, name, bases, attrs):
        new_cls = type.__new__(mcs, name, bases, attrs)
        new_cls.property_fields = []

        for attr in list(attrs) + sum([list(vars(base)) for base in bases], []):
            if attr.startswith('_') or attr in IGNORE_ATTRS:
                continue
            if isinstance(getattr(new_cls, attr), property):
                new_cls.property_fields.append(attr)
        return new_cls


class ModelMeta(_ModelMeta, PropertyHolder):
    ...


class BaseModel(Model, metaclass=ModelMeta):
    # 给予的默认字段
    id = fields.IntField(pk=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True
