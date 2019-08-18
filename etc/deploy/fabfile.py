"""
    by http://www.fabfile.org/index.html.
    fab deploy
"""
from pathlib import Path

from fabric import Connection, task
from invoke import Exit

# constant var
host_string = 'ubuntu@127.0.0.1'
home_dir = Path('path/to/ik-imgur/')
if not home_dir.exists():
    raise Exit("Aborting for: project path is not exists! Check the target param.")

python_env = Path('path/to/python')
if not python_env.exists():
    raise Exit("Aborting for: python file path is not exists! Check the virtualenv.")

conf = 'prod.conf'


@task
def deploy(ctx, branch=None):
    """
    :param ctx: default context for invoke.
    :param branch: target branch.
    :return:
    """
    if branch is None:
        branch = 'master'

    with Connection(host_string) as conn:
        print("Now Begin to deploy")
        conn.local(f"cd {home_dir}")

        # stop older worker.
        pid_file = 'var/run/ik-imgur.pid'
        conn.local(f"kill `cat {pid_file}`")
        print("You have stop gunicorn workers.")

        # git op
        print("Now fetching latest code.")
        conn.local("git fetch --all -p")
        conn.local(f"git reset --hard origin/{branch}")
        # run
        conn.local(f"{python_env}/bin/gunicorn {conf} wsgi:app -D")
        print(f"You have deployed latest code on Branch : {branch}")


@task
def stop(ctx):
    """
    :param ctx: default context for invoke.
    :return:
    """

    with Connection(host_string) as conn:
        print("Now Begin to stop gunicorn workers.")
        conn.local(f"cd {home_dir}")
        # kill current ik-imgur process.
        pid_file = 'var/run/ik-imgur.pid'
        conn.local(f"kill `cat {pid_file}`")
        print("You have stop gunicorn workers.")


@task
def start(ctx):
    """
    不拉取代码 直接启动
    :param ctx: default context for invoke.
    :return:
    """
    with Connection(host_string) as conn:
        conn.local(f"{python_env}/bin/gunicorn -c prod.conf wsgi:app -D")


@task
def restart(ctx):
    """
    不拉取代码 直接重新启动
    :param ctx: default context for invoke.
    :return:
    """
    stop(ctx)
    start(ctx)
    print("Restart Finish!")
