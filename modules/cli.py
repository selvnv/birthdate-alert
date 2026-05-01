import click

from modules.conf import App
from modules.db import Database
from modules.utils import print_table_paged
from modules.templates import render_birth_notification
from modules.messanger import send_telegram_birth_alert
from modules.logger import log


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
    log.info(f"Call add with parameters {name}, {birthdate}, {additional}")

    app = App("conf/app.yaml")
    db = Database(app.db_path)
    try:
        db.add(name, birthdate, additional)
    except Exception as error:
        print(f"\033[1m\033[93m[ERROR] >>>>\033[0m Error while add", error)
        log.error(f"Error while add", error)


@cli.command(name="list")
def lst():
    log.info(f"Call list")

    app = App("conf/app.yaml")
    db = Database(app.db_path)
    try:
        result = db.fetch_all()
        print_table_paged(result, headers=["Id", "Name", "Birthdate", "Additional Info"])
    except Exception as error:
        print(f"\033[1m\033[93m[ERROR] >>>>\033[0m Error while list", error)
        log.error(f"Error while list", error)


@cli.command(name="delete")
@click.argument("record_id", type=int, required=True)
def remove(record_id):
    log.info(f"Call remove with parameters {record_id}")

    app = App("conf/app.yaml")
    db = Database(app.db_path)
    try:
        result = db.remove(record_id)
        print_table_paged(result, headers=["Id", "Name", "Birthdate", "Additional Info"])
    except Exception as error:
        print(f"\033[1m\033[93m[ERROR] >>>>\033[0m Error while delete", error)
        log.error(f"Error while delete", error)


@cli.command(name="today")
def today():
    log.info(f"Call today")

    app = App("conf/app.yaml")
    db = Database(app.db_path)

    try:
        result = db.get_today_births()
        print_table_paged(result, headers=["Id", "Name", "Birthdate", "Additional Info"])
    except Exception as error:
        print(f"\033[1m\033[93m[ERROR] >>>>\033[0m Error while show today births", error)
        log.error(f"Error while show today births", error)


@cli.command(name="alert")
def alert():
    log.info(f"Call alert")

    app = App("conf/app.yaml")
    db = Database(app.db_path)

    try:
        result = db.get_today_births()
        for record in result:
            name, birthdate, additional_info = record
            print(name, birthdate, additional_info)

            message_html = render_birth_notification(
                template_path=app.alert_template_path,
                name=name,
                birthdate=birthdate,
                additional_info=additional_info or "Ничо не написали=("
            )

            send_telegram_birth_alert(message_html)
    except Exception as error:
        print(f"\033[1m\033[93m[ERROR] >>>>\033[0m Error while alert today births", error)
        log.error(f"Error while alert today births", error)
