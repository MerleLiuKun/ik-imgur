from tortoise import fields
from tortoise.models import Model
from tortoise.models import ModelMeta as _ModelMeta


class PropertyHolder(type):
    """
    定义元类 用于为 Model 的基类补充默认字段
    This follow https://github.com/dongweiming/lyanna/blob/master/models/base.py
    """

    def __new__(mcs, name, bases, attrs):
        new_cls = type.__new__(mcs, name, bases, attrs)
        new_cls.property_fields = []

        for attr in list(attrs) + sum([list(vars(base)) for base in bases], []):
            if attr.startswith('_'):
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
