import click

from modules.db import Database


@click.group()
def cli():
    pass


@cli.command(name="init")
@click.option("--file", "-f", type=click.File("r"))
def init(file):
    db = Database("birthday_info", "db", "birthday_info")
    db.init(file)


@cli.command(name="add")
def add():
    pass


@cli.command(name="list")
def lst():
    db = Database("birthday_info", "db", "birthday_info")
    result = db.fetch_all()
    print(result)


@cli.command(name="delete")
def remove():
    pass
