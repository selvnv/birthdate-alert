import yaml
from pathlib import Path

class App:
    def __init__(self, config_path):
        self._config_path = Path(config_path)
        self._db_path = None
        self._schema_path = None

        self._load_settings_from_file(self._config_path)


    def __repr__(self) -> str:
        return (
            f"App("
            f"config_path: {self.config_path}, "
            f"db_path: {self.db_path}"
            f"schema_path: {self.schema_path}"
            f")"
        )


    @property
    def db_path(self):
        return self._db_path


    @property
    def config_path(self):
        return self._config_path


    @property
    def schema_path(self):
        return self._schema_path


    def _load_settings_from_file(self, path: Path) -> None:

        if path.suffix.lower() not in [".yaml", ".yml"]:
            raise Exception(f"\033[1m\033[91m[WARN]\033[0m App config must be .yaml/.yml format")

        if not path.exists():
            raise Exception(f"\033[1m\033[91m[WARN]\033[0m Wrong app config file path")

        if not path.is_file():
            raise Exception(f"\033[1m\033[91m[WARN]\033[0m Config path is not a file")

        try:
            with path.open("r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

                if config is None:
                    raise Exception(f"\033[1m\033[91m[WARN]\033[0m Config file is empty: {path}")

                if "sqlite" not in config:
                    raise Exception(f"\033[1m\033[91m[WARN]\033[0m Missing 'sqlite' section in config")

                self._db_path = config["sqlite"]["db_path"]
                self._schema_path = config["sqlite"]["schema_path"]
        except yaml.YAMLError as error:
            raise Exception(f"\033[1m\033[91m[WARN]\033[0m Invalid YAML syntax in {path}: {error}")
        except Exception as error:
            raise Exception(f"\033[1m\033[91m[WARN]\033[0m Unexpected error reading config: {error}")