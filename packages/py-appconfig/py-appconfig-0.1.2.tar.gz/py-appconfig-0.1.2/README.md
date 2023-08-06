# py-AppConfig

Persistent configuration storage for python applications. Based on similar `npm` modules,
because of the lack of a `python` package that does something similar.

> **Note**: This package is still under development. Core functions work just fine,
> and as intended. But a few QOL features need to be worked in.

### Installation

```sh
# still in testing, pip package coming soon
pip install py-appconfig

# for now, package is active and working on TestPyPI
pip install -i https://test.pypi.org/simple/ py-appconfig
```

### Usage

```py
from appconfig import AppConfig

config = AppConfig(project_name="myProject", defaults={'a': 10, 'b': 'this is a b'})
config_values = {
    'number': 1234,
    'string': 'some random string'
}

for item in config_values:
    config.set(item, config_values[item])

print(config.get_all())
print(config.get('number'))
print(config.get('string'))

# reset and delete config values
config.reset('a')
config.reset_all()
config.delete('string')
```

### Option/args during init

1. `project_name` : `str` -> **required**
2. `project_id`: `str` -> *optional*, default = `project_name`
3. `version`: `str` -> *optional*, default = `0.0.1`
4. `conf_name`: `str` -> *optional*, default = `config` (filename of config file)
5. `conf_ext`: `str` -> *optional*, default = `.json` (file extension for config file)
6. `verbose`: `bool` -> *optional*, default = `False` (for verbose logging, needs more work)
7. `defaults`: `dict` -> *optional*, no default value, can be used to set project default settings

>Note: 2 and 3 not necessary, but may be used later for project config identification and things like version migration

### Module functions

```py
from appconfig import AppConfig

config = AppConfig(project_name="myProject")

config.set('key', 'value')
config.get('key')
config.get_all()
```

### To-do

1. Atomically writing configs to prevent corruptions due to runtime errors or system crashes.
2. A better validation system for config values. Right now it only makes sure it does not try to store a function.
3. Type annotations. (partially done)


## Related

Loosely based on the same basic concept as some `npm` packages commonly used with javascript applications.
- [`conf`](https://github.com/sindresorhus/conf) and [`appconfig`](https://raw.githubusercontent.com/anujdatar/appconfig).

## License

[MIT](https://github.com/anujdatar/py-appconfig/blob/master/LICENSE) Copyright (c) 2019-2021 Anuj Datar
