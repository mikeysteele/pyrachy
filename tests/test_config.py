import pytest
import sys
from unittest.mock import patch, mock_open

from pyrachy import Pyrachy, ArgvLoader, DictLoader, EnvLoader, FileLoader

# Test Config class and loaders


@pytest.fixture
def mock_yaml_file():
    file_contents = """
    db:
      host: localhost
      port: 5432
    """
    with patch("builtins.open", mock_open(read_data=file_contents)):
        yield file_contents


@pytest.fixture
def mock_toml_file():
    file_contents = """
    [db]
    host = "localhost"
    port = 5432
    """
    with patch("builtins.open", mock_open(read_data=file_contents)):
        yield file_contents


# Test DictLoader
def test_dict_loader():
    loader = DictLoader({"db": {"host": "localhost", "port": "5432"}})
    config = Pyrachy([loader])
    loaded_config = config.get()

    assert loaded_config == {"db": {"host": "localhost", "port": "5432"}}


# Test DictLoader getting single arg
def test_dict_loader_with_arg():
    loader = DictLoader({"db": {"host": "localhost", "port": "5432"}})
    config = Pyrachy([loader])
    loaded_config = config.get("db")

    assert loaded_config == {"host": "localhost", "port": "5432"}


# Test DictLoader getting single arg
def test_dict_loader_with_arg_with_dot():
    loader = DictLoader({"db": {"host": "localhost", "port": "5432"}})
    config = Pyrachy([loader])
    loaded_config = config.get("db.host")

    assert loaded_config == "localhost"


# Test ArgLoader
def test_arg_loader(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        sys, "argv", [sys.argv[0], "--db-host=localhost", "--db-port=5432"]
    )
    arg_loader = ArgvLoader(allowed_args=["db-host", "db-port"], separator="-")
    config = Pyrachy([arg_loader])
    loaded_config = config.get()

    assert loaded_config == {"db": {"host": "localhost", "port": "5432"}}


# Test EnvLoader
def test_env_loader(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MY_APP_db_host", "localhost")
    monkeypatch.setenv("MY_APP_db_port", "5432")

    env_loader = EnvLoader(prefix="MY_APP_", separator="_")
    config = Pyrachy([env_loader])
    loaded_config = config.get()

    assert loaded_config == {"db": {"host": "localhost", "port": "5432"}}


# # Test FileLoader with YAML
# def test_file_loader_yaml():

#     loader = FileLoader(file_paths=['config.yaml'])
#     config = Pyrachy([loader])
#     loaded_config = config.get()

#     assert loaded_config == {'db': {'host': 'localhost', 'port': 5432}}

# # Test FileLoader with TOML
# def test_file_loader_toml():
#     loader = FileLoader(file_paths=['config.toml'])
#     config = Pyrachy([loader])
#     loaded_config = config.get()

#     assert loaded_config == {'db': {'host': 'localhost', 'port': 5432}}


# Test multiple loaders
def test_multiple_loaders(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        sys, "argv", [sys.argv[0], "--db-host=localhost", "--db-port=5432"]
    )
    monkeypatch.setenv("MY_APP_db_host", "localhost")
    monkeypatch.setenv("MY_APP_db_port", "5433")
    arg_loader = ArgvLoader(allowed_args=["db-host"], separator="-")
    env_loader = EnvLoader(prefix="MY_APP_", separator="_")
    config = Pyrachy([arg_loader, env_loader])
    loaded_config = config.get()

    assert loaded_config == {"db": {"host": "localhost", "port": "5433"}}
