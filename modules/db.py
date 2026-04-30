import sqlite3
from pathlib import Path
from datetime import datetime


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
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1;")

            return True

        except Exception as error:
            print(f"\033[1m\033[91m[WARN]\033[0m Healthcheck failed", error)
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
            raise ValueError(f"Wrong file path {initial_sql_file}")


    def add(self, name: str, birthdate: datetime, add_info: str):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = f"""
                INSERT INTO birthday_info (name, birthdate, additional_info) 
                VALUES (?, ?, ?)
                RETURNING id;
            """
            cursor.execute(query, (name, birthdate.strftime('%Y-%m-%d'), add_info))

            # Return new item id
            return cursor.fetchone()[0]


    def remove(self, record_id: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = f"""
            DELETE FROM birthday_info
            WHERE id = ?
            RETURNING id;
            """

            cursor.execute(query, (record_id,))

            # Return deleted item id
            return cursor.fetchone()[0]


    def fetch_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            query = f"SELECT * FROM birthday_info"
            cursor.execute(query)

            result = cursor.fetchall()
            return result