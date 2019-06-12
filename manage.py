"""
    封装常见的命令
"""

import click
import hashlib
from tortoise import Tortoise, run_async
from tortoise.exceptions import IntegrityError

from app.extensions import init_db
from app.models.user import create_user


async def init():
    await init_db(create_db=False)
    await Tortoise._drop_databases()
    await init_db(create_db=True)
    await Tortoise.generate_schemas()


@click.group()
def cli():
    pass


@cli.command()
def initdb():
    run_async(init())
    click.echo('The database initialed.')


async def _add_user(**kwargs):
    await init_db()
    try:
        user = await create_user(**kwargs)
    except IntegrityError as e:
        click.echo(str(e))
    else:
        click.echo(f'User {user.username} created!!! ID: {user.id}')


@cli.command()
@click.option('--name', required=True, prompt=True)
@click.option('--password', required=True, prompt=True, confirmation_prompt=True)
@click.option('--email', required=True, prompt=True)
def adduser(name, password, email):
    if password is None:
        password = ''
    password = hashlib.md5(password.encode('utf-8')).hexdigest()
    run_async(_add_user(username=name, password=password, email=email))


if __name__ == '__main__':
    cli()
