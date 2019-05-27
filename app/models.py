from tortoise import fields
from tortoise.models import Model

from app.utils.path_handler import generate_hash_id, generate_hash_name


class BaseModel(Model):
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Image(BaseModel):
    hash_id = fields.CharField(max_length=100)
    name = fields.CharField(max_length=255)  # stored name
    filename = fields.CharField(max_length=255)  # source name
    size = fields.IntField(default=0)
    width = fields.IntField(default=0)
    height = fields.IntField(default=0)
    path = fields.CharField(max_length=255, null=True)

    class Meta:
        table = 'image'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Image(ID={self.hash_id}, filename={self.filename})"

    @classmethod
    async def create(cls, **kwargs):
        """
        :param kwargs: image params
        :return:
        """
        if 'hash_id' not in kwargs:
            kwargs['hash_id'] = await generate_hash_id()
        obj = await super().create(**kwargs)
        return obj


async def create_image(**data):
    if 'filename' not in data:
        raise ValueError('filename is required.')
    if 'name' not in data and 'path' not in data:
        name, path_prefix = generate_hash_name(data['filename'])
        data['name'], data['path'] = name, path_prefix + name
    img = await Image.create(**data)
    return img
