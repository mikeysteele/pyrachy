import sys
from typing import List, Dict, Any, Optional
from .base_loader import BaseLoader


class ArgvLoader(BaseLoader):
    def __init__(
        self,
        prefix: str = "--",
        separator: Optional[str] = None,
        allowed_args: Optional[List[str]] = None,
    ):
        """
        Args:
            allowed_args (List[str], optional): List of argument names to extract (e.g., ["database.host", "debug"]).
            prefix (str, optional): Prefix for arguments (e.g., "--config-key"). Defaults to "--".
        """
        self.allowed_args = allowed_args
        self.prefix = prefix
        self.separator = separator

    def load(self) -> Dict[str, Any]:

        parsed_args: Dict[str, Any] = {}
        argv = sys.argv[1:]  # Get actual shell arguments

        for arg in argv:
            if arg.startswith(self.prefix):
                key_value = arg[len(self.prefix) :].split("=", 1)
                key = key_value[0]
                value = (
                    key_value[1] if len(key_value) > 1 else True
                )  # Handle boolean flags

                if self.allowed_args is not None and key not in self.allowed_args:
                    continue

                self._set_nested(parsed_args, key.split(self.separator), value)

        return parsed_args
