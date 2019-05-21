"""
    封装常见的命令
"""

import click
from tortoise import Tortoise, run_async
from tortoise.exceptions import IntegrityError

from app.extensions import init_db
from app.models import create_image


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


async def _add_img(**kwargs):
    await init_db()
    try:
        img = await create_image(**kwargs)
    except IntegrityError as e:
        click.echo(str(e))
    else:
        click.echo(f'Image {img.name} created!!! ID: {img.id}')


@cli.command()
@click.option('--name', required=True, prompt=True)
def add_img(name):
    run_async(_add_img(name=name))


if __name__ == '__main__':
    cli()
