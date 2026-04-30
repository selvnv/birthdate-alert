import click

from modules.conf import App
from modules.db import Database
from modules.utils import print_table_paged


@click.group()
def cli():
    pass


@cli.command(name="init")
def init():
    app = App("conf/app.yaml")
    db = Database(app.db_path)
    db.init(app.schema_path)


@cli.command(name="add")
@click.option("--name", "-n", type=str, required=True)
@click.option("--birthdate", "-b", type=click.DateTime(formats=["%Y-%m-%d"]), required=True)
@click.option("--additional", "-a", type=str, required=False, default=None)
def add(name, birthdate, additional):
    app = App("conf/app.yaml")
    db = Database(app.db_path)
    try:
        db.add(name, birthdate, additional)
    except Exception as error:
        print(f"\033[1m\033[93m[ERROR] >>>>\033[0m Error while add", error)


@cli.command(name="list")
def lst():
    app = App("conf/app.yaml")
    db = Database(app.db_path)

    try:
        result = db.fetch_all()
        print_table_paged(result, headers=["Id", "Name", "Birthdate", "Additional Info"])
    except Exception as error:
        print(f"\033[1m\033[93m[ERROR] >>>>\033[0m Error while list", error)


@cli.command(name="delete")
@click.argument("record_id", type=int, required=True)
def remove(record_id):
    app = App("conf/app.yaml")
    db = Database(app.db_path)
    try:
        result = db.remove(record_id)
        print_table_paged(result, headers=["Id", "Name", "Birthdate", "Additional Info"])
    except Exception as error:
        print(f"\033[1m\033[93m[ERROR] >>>>\033[0m Error while delete", error)
