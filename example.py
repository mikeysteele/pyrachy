
from src.pyrachy import Pyrachy
from src.loaders.dict_loader import DictLoader
from src.loaders.env_loader import EnvLoader
from src.loaders.argv_loader import ArgvLoader
from src.loaders.file_loader import FileLoader

def main():
    config = Pyrachy([        
        DictLoader({
            "name": "Me",
            "db": {
                "host": 123,
                "port": 234
            }
        }),
        EnvLoader("PY_", "__"),
        ArgvLoader(separator="-"),
        FileLoader(["pyproject.toml"])
    ])
    print(config.get())


if __name__ == "__main__":
    main()
