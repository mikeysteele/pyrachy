from abc import ABC, abstractmethod
from typing import Any


class BaseLoader(ABC):
    @abstractmethod
    def load(self) -> dict[str, Any]:
        return {}

    def _set_nested(self, data: dict[str, Any], keys: list[str], value: Any):
        """Recursively set values in a nested dictionary."""
        current = data
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def _merge_dicts(self, base: dict[str, Any], new_data: dict[str, Any]):
        """
        Recursively merge new_data into base.
        """
        for key, value in new_data.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._merge_dicts(base[key], value)  # type: ignore
            else:
                base[key] = value
