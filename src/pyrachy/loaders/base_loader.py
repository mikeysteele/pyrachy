from abc import ABC, abstractmethod
from typing import Dict, List, Any


class BaseLoader(ABC):
    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """Load configuration and return a nested dictionary."""
        pass

    def _set_nested(self, data: Dict[str, Any], keys: List[str], value: Any):
        """Recursively set values in a nested dictionary."""
        current = data
        for key in keys[:-1]:
            if key not in current or not isinstance(current[key], dict):
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def _merge_dicts(self, base: Dict[str, Any], new_data: Dict[str, Any]):
        """
        Recursively merge new_data into base.
        """
        for key, value in new_data.items():
            if isinstance(value, dict) and key in base and isinstance(base[key], dict):
                self._merge_dicts(base[key], value)
            else:
                base[key] = value
