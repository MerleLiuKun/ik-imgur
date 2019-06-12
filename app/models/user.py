from tortoise import fields
from tortoise.query_utils import Q
from werkzeug.security import check_password_hash, generate_password_hash

from .base import BaseModel


class User(BaseModel):
    username = fields.CharField(max_length=100, unique=True)
    nickname = fields.CharField(max_length=100, default='')
    password_hash = fields.CharField(max_length=255)
    email = fields.CharField(max_length=100, default='')
    avatar = fields.CharField(max_length=255, default='')
    active = fields.BooleanField(default=True)

    class Meta:
        table = 'users'

    def __str__(self):
        return self.username

    def __repr__(self):
        return f"User(ID={self.id}, username={self.username})"


def generate_password(password):
    return generate_password_hash(password)


async def create_user(**data):
    if 'username' not in data or 'password' not in data:
        raise ValueError('username and password must provide')
    data['password_hash'] = generate_password_hash(data.pop('password'))

    user = await User.create(**data)

    return user


async def validate_login(username, password):
    user = await User.filter(
        Q(username=username) | Q(email=username)
    ).first()
    if not user:
        return False, None
    if check_password_hash(user.password, password):
        return True, user
    return False, None
