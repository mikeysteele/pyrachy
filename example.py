from pyrachy import Pyrachy, dictLoader, EnvLoader, ArgvLoader, FileLoader


def main():
    config = Pyrachy(
        [
            dictLoader({"name": "Me", "db": {"host": 123, "port": 234}}),
            EnvLoader("PY_", "__"),
            ArgvLoader(separator="-"),
            FileLoader(["pyproject.toml"]),
        ]
    )
    print(config.get())
    print(config.get("db"))
    print(config.get("db.host"))


if __name__ == "__main__":
    main()
