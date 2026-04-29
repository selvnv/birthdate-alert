import sqlite3
from pathlib import Path
from datetime import datetime

from modules.utils import get_env_value, clean_env_value


class Database:
    _DATABASE_ENV_VARIABLE_NAMES = [
        "DATABASE_NAME",
        "DATABASE_CATALOG",
        "TABLE_NAME"
    ]

    def __init__(
            self,
            dbname: str = "",
            dbcatalog: str = "",
            table_name: str = ""):
        self._dbname = dbname

        if dbcatalog and dbcatalog.endswith('/'):
            self._dbcatalog = dbcatalog
        else:
            self._dbcatalog = dbcatalog + "/"

        self._table_name = table_name


    def __repr__(self):
        return (
            f"Database({self.dbname}, {self.dbcatalog})\n)"
        )


    @property
    def dbname(self):
        return self._dbname


    @property
    def dbcatalog(self):
        return self._dbcatalog


    @property
    def table_name(self):
        return self._table_name


    @property
    def db_path(self):
        if self._dbcatalog and not self._dbcatalog.endswith('/'):
            return f"{self._dbcatalog}/{self._dbname}"
        return f"{self._dbcatalog}{self._dbname}"


    def healthcheck(self) -> bool:
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1;")

            return True

        except Exception as error:
            print(f"\033[1m\033[91m[WARN]\033[0m Healthcheck failed", error)
            return False


    def get_connection(self) -> sqlite3.Connection | None:
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
        except Exception as error:
            print(f"\033[1m\033[91m[WARN] get_connection(...) >>>>\033[0m Connection failed", repr(error))

        return conn


    def load_settings_from_env(self):
        loaded_variables = {}

        for variable_name in self._DATABASE_ENV_VARIABLE_NAMES:
            loaded_variables[variable_name] = get_env_value(variable_name)

        for var_name, var_value in loaded_variables.items():
            if not var_value:
                print(f"\033[1m\033[91m[WARN] load_settings_from_env(...) >>>>\033[0m Trying to assign empty value {type(var_value)} to {var_name}")
                return

        self._dbname = loaded_variables["DATABASE_NAME"]
        self._dbcatalog = loaded_variables["DATABASE_CATALOG"]
        self._table_name = loaded_variables["TABLE_NAME"]


    def load_settings_from_file(self, file_path: str):
        path = Path(file_path)

        if path.exists() and path.is_file():
            with open(path, "r") as file:
                for line in file:
                    clear_line = line.strip()

                    if not clear_line:
                        continue

                    if clear_line.startswith("#"):
                        continue

                    arg, value = clear_line.split("=", maxsplit=1)

                    cleaned_arg = clean_env_value(arg)
                    cleaned_value = clean_env_value(value)

                    if cleaned_arg == "DATABASE_NAME":
                        self._dbname = cleaned_value
                    elif cleaned_arg == "DATABASE_CATALOG":
                        self._dbcatalog = cleaned_value
                    elif cleaned_arg == "TABLE_NAME":
                        self._table_name = cleaned_value
                    else:
                        print(
                            f"\033[1m\033[93m[WARN] load_settings_from_file() >>>>\033[0m Unknown config parameter {cleaned_arg}")
        else:
            raise ValueError(f"Wrong file path {file_path}")


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
                INSERT INTO {self._table_name} (name, birthdate, additional_info) 
                VALUES (?, ?, ?)
                RETURNING id;
            """
            cursor.execute(query, (name, birthdate.strftime('%Y-%m-%d'), add_info))

            # Return new item id
            return cursor.fetchone()[0]

    def remove(self):
        pass


    def fetch_all(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            query = f"SELECT * FROM {self._table_name}"
            cursor.execute(query)

            result = cursor.fetchall()
            return result