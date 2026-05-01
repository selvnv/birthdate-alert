import sqlite3
from pathlib import Path
from datetime import datetime


from modules.logger import log


class Database:

    def __init__(self, db_path: str = "",):
        self._db_path = db_path


    def __repr__(self):
        return (
            f"Database({self.db_path})\n)"
        )


    @property
    def db_path(self) -> str:
        return self._db_path


    def healthcheck(self) -> bool:
        try:
            log.info("Start healthcheck")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1;")

            log.info("Finish healthcheck")
            return True

        except Exception as error:
            log.warn(f"\033[1m\033[91m[WARN]\033[0m Healthcheck failed", error)
            return False


    def init(self, initial_sql_file: str):
        path = Path(initial_sql_file)

        if path.exists() and path.is_file():
            with open(path, "r") as file:
                query = file.read()

                with sqlite3.connect(self.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(query)
        else:
            log.error(f"\033[1m\033[91m[WARN]\033[0m Wrong init sql file path {initial_sql_file}")
            raise ValueError(f"Wrong file path {initial_sql_file}")


    def add(self, name: str, birthdate: datetime, add_info: str):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                    INSERT INTO birthday_info (name, birthdate, additional_info) 
                    VALUES (?, ?, ?)
                    RETURNING id;
                """
                log.info(f"Run query {query} with params {name}, {birthdate.strftime('%Y-%m-%d')}, {add_info}")
                cursor.execute(query, (name, birthdate.strftime('%Y-%m-%d'), add_info))

                # Return new item id
                return cursor.fetchone()[0]
        except Exception as error:
            log.error(f"\033[1m\033[91m[WARN]\033[0m Database add operation error: {error}")
            raise error



    def remove(self, record_id: int):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                DELETE FROM birthday_info
                WHERE id = ?
                RETURNING id;
                """

                log.info(f"Run query {query} with params {record_id}")
                cursor.execute(query, (record_id,))

                # Return deleted item id
                return cursor.fetchone()[0]
        except Exception as error:
            log.error(f"\033[1m\033[91m[WARN]\033[0m Database delete operation error: {error}")
            raise error


    def fetch_all(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                query = f"SELECT * FROM birthday_info"
                log.info(f"Run query {query}")
                cursor.execute(query)

                result = cursor.fetchall()
                return result
        except Exception as error:
            log.error(f"\033[1m\033[91m[WARN]\033[0m Database fetch all operation error: {error}")
            raise error



    def get_today_births(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                today = datetime.today()
                query = f"""
                    SELECT name, birthdate, additional_info
                    FROM birthday_info
                    WHERE birthdate LIKE ?
                """

                log.info(f"Run query {query} with params %{today.strftime('-%m-%d')}")
                cursor.execute(query, ("%" + today.strftime('-%m-%d'),))

                return cursor.fetchall()
        except Exception as error:
            log.error(f"\033[1m\033[91m[WARN]\033[0m Database get today births operation error: {error}")
            raise error
