import os
from typing import Any
from .base_loader import BaseLoader


class EnvLoader(BaseLoader):
    def __init__(self, prefix: str = "", separator: str = "__"):
        """
        Args:
            prefix (str, optional): Prefix for environment variables (e.g., "APP_").
            separator (str, optional): Separator to split nested keys (e.g., "DB__HOST" → {"DB": {"HOST": value}}).
        """
        self.prefix = prefix
        self.separator = separator

    def load(self) -> dict[str, Any]:

        parsed_env: dict[str, Any] = {}

        for key, value in os.environ.items():
            if self.prefix and not key.startswith(self.prefix):
                continue  # Skip variables without the required prefix

            env_key = key[len(self.prefix) :] if self.prefix else key
            self._set_nested(parsed_env, env_key.split(self.separator), value)

        return parsed_env
