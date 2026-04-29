import click

from modules.db import Database


@click.group()
def cli():
    pass


@cli.command(name="init")
@click.option("--file", "-f", type=str, required=True)
def init(file):
    db = Database("birthday_info", "db", "birthday_info")
    db.init(file)


@cli.command(name="add")
@click.option("--name", "-n", type=str, required=True)
@click.option("--birthdate", "-b", type=click.DateTime(formats=["%Y-%m-%d"]), required=True)
@click.option("--additional", "-a", type=str, required=False, default=None)
def add(name, birthdate, additional):
    db = Database("birthday_info", "db", "birthday_info")
    try:
        db.add(name, birthdate, additional)
    except Exception as error:
        print(f"\033[1m\033[93m[ERROR] >>>>\033[0m Error while add", error)


@cli.command(name="list")
def lst():
    db = Database("birthday_info", "db", "birthday_info")
    try:
        result = db.fetch_all()
        print(result)
    except Exception as error:
        print(f"\033[1m\033[93m[ERROR] >>>>\033[0m Error while list", error)


@cli.command(name="delete")
def remove():
    pass
