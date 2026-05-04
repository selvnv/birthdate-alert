import yaml
from pathlib import Path

class App:
    def __init__(self, config_path):
        self._config_path = Path(config_path)
        self._db_path = None
        self._schema_path = None

        self._telegram_token = None
        self._telegram_chat_id = None

        self._alert_template_path = None

        self._load_settings_from_file(self._config_path)


    def __repr__(self) -> str:
        return (
            f"App("
            f"config_path={self.config_path}, "
            f"db_path={self.db_path}, "
            f"schema_path={self.schema_path}, "
            f"telegram_token={self.telegram_token}, "
            f"telegram_chat_id={self.telegram_chat_id}, "
            f"template_path={self.alert_template_path}"
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


    @property
    def alert_template_path(self):
        return self._alert_template_path


    @property
    def telegram_token(self):
        return self._telegram_token

    @property
    def telegram_chat_id(self):
        return self._telegram_chat_id


    def _load_settings_from_file(self, path: Path) -> None:

        if path.suffix.lower() not in [".yaml", ".yml"]:
            raise Exception(f"App config must be .yaml/.yml format")

        if not path.exists():
            raise Exception(f"Wrong app config file path")

        if not path.is_file():
            raise Exception(f"Config path is not a file")

        try:
            with path.open("r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

                if config is None:
                    raise Exception(f"Config file is empty: {path}")

                if "sqlite" not in config:
                    raise Exception(f"Missing 'sqlite' section in config")

                if "telegram" not in config:
                    raise Exception(f"Missing 'telegram' section in config")

                if "app" not in config:
                    raise Exception(f"Missing 'app' section in config")

                self._db_path = config["sqlite"]["db_path"]
                self._schema_path = config["sqlite"]["schema_path"]

                self._telegram_token = config["telegram"]["token"]
                self._telegram_chat_id = config["telegram"]["chat_id"]

                self._alert_template_path = config["app"]["notification_template"]
        except yaml.YAMLError as error:
            raise Exception(f"\033[1m\033[93m[WARN]\033[0m  Invalid YAML syntax in {path}: {error}")
        except Exception as error:
            raise Exception(f"\033[1m\033[93m[WARN]\033[0m  Unexpected error while reading config: {error}")