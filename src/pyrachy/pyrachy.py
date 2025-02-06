from typing import Any, Optional, Union
from .loaders.base_loader import BaseLoader


class Pyrachy:
    def __init__(self, loaders: list[BaseLoader]):
        self.loaders = loaders
        merged_data: dict[str, Any] = {}

        for loader in loaders:  # Preserve priority
            if not isinstance(loader, BaseLoader):  # type: ignore
                raise TypeError(f"{loader} must subclass BaseLoader")
            merged_data = self._merge_dicts(merged_data, loader.load())

        self.__config = merged_data  # Store as a nested dict

    def _merge_dicts(self, base: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
        """Recursively merge two dictionaries (new overrides base)."""
        for key, value in new.items():
            if isinstance(value, dict) and isinstance(base.get(key), dict):
                base[key] = self._merge_dicts(base[key], value)  # type: ignore
            else:
                base[key] = value
        return base

    def get(
        self, key: Optional[str] = None, default: Optional[str] = None
    ) -> Union[Any, None]:
        """Retrieve a nested key using dot notation."""
        d: Any = self.__config
        if key is not None:
            keys = key.split(".")
            for k in keys:
                if not isinstance(d, dict) or k not in d:
                    return default
                d = d[k]  # type: ignore
        return d
