import os
import yaml
from threading import Lock


class ConfigManager:
    _config = None
    _lock = Lock()

    @classmethod
    def load(cls):
        if cls._config is None:
            with cls._lock:
                if cls._config is None:
                    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config"))
                    config_file = os.path.join(base_path, "config.yaml")

                    with open(config_file, "r") as file:
                        cls._config = yaml.safe_load(file)

    @classmethod
    def get_url(cls, key):
        return cls._config["urls"].get(key)

    @classmethod
    def get_credential(cls, key):
        return cls._config["credentials"].get(key)

    @classmethod
    def get_timeout(cls, key):
        return cls._config["timeouts"].get(key)

    @classmethod
    def get_retry_count(cls, key):
        return cls._config["retries"].get(key)

    @classmethod
    def get(cls, *keys):
        data = cls._config
        for key in keys:
            if data is None:
                return None
            data = data.get(key)
        return data
