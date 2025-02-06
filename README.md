# Pyrachy - Hierarchical Config Loader

This Python package provides a flexible, pluggable configuration system that loads configuration from multiple sources such as command-line arguments, environment variables, and files (YAML, TOML, etc.). It is designed to support hierarchical configuration structures, making it easy to manage complex configurations in your Python projects.

## Features

- **Hierarchical Configuration**: Supports nested configuration values for more complex setups.
- **Pluggable Loaders**: Easily extendable system with support for multiple configuration sources such as command-line arguments, environment variables, and files.
- **Extensible**: Freedom to create your own loaders which can load config from anywhere.


## Usage
1. Define Loaders
The core of the system is the loader class that fetches the configuration from various sources. Each loader implements the BaseLoader class and is responsible for loading the configuration from a specific source.

### Included Loaders
* ArgvLoader: Loads configuration from command-line arguments.
* EnvLoader: Loads configuration from environment variables.
* FileLoader: Loads configuration from files (YAML, TOML, JSON).
2. Create the Config Object
You can create a Config object and pass a list of loaders. The Pyrachy class will try to load the configuration from each of the defined loaders and merge them into a single configuration, from right to left

Example
```python
from pyrachy import Pyrachy, ArgLoader, EnvLoader, FileLoader

# Create the loaders
arg_loader = ArgvLoader(allowed_args=['db-host', 'db-port'], separator='-')
env_loader = EnvLoader(prefix="MY_APP_", separator='_')
file_loader = FileLoader(file_paths=['config.yaml'])

# Create the Config object and load the configuration
config = Pyrachy([   
    file_loader,
    arg_loader, 
    env_loader, 
])
loaded_config = config.get()

print(loaded_config)
```
In this example, the Config object will load configuration values from:

1. Environment variables: e.g., MY_APP_db_port=5433
2. Command-line arguments: e.g., --db-host=remote --db-port=5432
3. YAML file: e.g., a file config.yaml with contents:

```yml
db:
  host: localhost
  port: 5432
  dbname: test
```
The result will be a single merged configuration:

```python
{
  'db': {
    'host': 'remote',
    'port': '5433',
    'dbname': 'test'
  }
}
```
## Custom Loaders
You can easily extend this package by adding custom loaders. Each loader should inherit from the BaseLoader class and implement the load() method.

```python
from Pyrachy import BaseLoader

class CustomLoader(BaseLoader):
    def load(self) -> dict[str, Any]:
        # Custom logic to load configuration
        return {'custom': {'value': 'example'}}
```

## Contributing

We welcome contributions to improve the project! Please follow these guidelines to get started:

### 1. Fork the repository

Start by forking the repository to your own GitHub account. This will allow you to make changes and submit a pull request.

### 2. Install dependencies
Make sure you have all required development dependencies installed. This project uses [uv](https://docs.astral.sh/uv/)
 for dependency management

To install it, you can run: `pipx install uv`


Then run `uv sync` to install required packages


### 3. Make your changes
Implement your changes or improvements. Ensure your code adheres to the project's style guide and that any new features are thoroughly tested.

### 4. Write tests
Add tests for any new features or changes. We use pytest for testing, so please ensure that your tests are written with pytest.

You can run the tests using pytest. The tests cover the core functionality and ensure that the loaders work correctly with different configuration sources.
```bash
uv run task test

```

### 5. Commit your changes
Commits MUST follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
 standard. Example commit types include:

* feat: A new feature
* fix: A bug fix
* chore: Routine tasks like updates to dependencies or documentation
* docs: Changes to documentation
* style: Code style improvements (e.g., formatting, linting)
* test: Adding or improving tests
* refactor: Refactoring code without changing functionality

This repo includes [commitizen](https://commitizen-tools.github.io/commitizen/)
 to help you write conventional commits

### 6. Create a pull request
Open a pull request from your branch to the main branch of the original repository. Provide a detailed description of the changes and why they are needed.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.