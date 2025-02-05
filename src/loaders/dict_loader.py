from typing import Dict, Any
from .base_loader import BaseLoader


class DictLoader(BaseLoader):
    def __init__(self, config_dict: Dict[str, Any]):
        if not isinstance(config_dict, dict):  # type: ignore
            raise TypeError("DictLoader requires a dictionary")
        self.config_dict = config_dict

    def load(self) -> Dict[str, Any]:
        return self.config_dict
