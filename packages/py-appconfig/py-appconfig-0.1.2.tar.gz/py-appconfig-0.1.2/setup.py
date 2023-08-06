# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['appconfig']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'py-appconfig',
    'version': '0.1.2',
    'description': 'Persistent configuration storage for python applications',
    'long_description': '# py-AppConfig\n\nPersistent configuration storage for python applications. Based on similar `npm` modules,\nbecause of the lack of a `python` package that does something similar.\n\n> **Note**: This package is still under development. Core functions work just fine,\n> and as intended. But a few QOL features need to be worked in.\n\n### Installation\n\n```sh\n# still in testing, pip package coming soon\npip install py-appconfig\n\n# for now, package is active and working on TestPyPI\npip install -i https://test.pypi.org/simple/ py-appconfig\n```\n\n### Usage\n\n```py\nfrom appconfig import AppConfig\n\nconfig = AppConfig(project_name="myProject", defaults={\'a\': 10, \'b\': \'this is a b\'})\nconfig_values = {\n    \'number\': 1234,\n    \'string\': \'some random string\'\n}\n\nfor item in config_values:\n    config.set(item, config_values[item])\n\nprint(config.get_all())\nprint(config.get(\'number\'))\nprint(config.get(\'string\'))\n\n# reset and delete config values\nconfig.reset(\'a\')\nconfig.reset_all()\nconfig.delete(\'string\')\n```\n\n### Option/args during init\n\n1. `project_name` : `str` -> **required**\n2. `project_id`: `str` -> *optional*, default = `project_name`\n3. `version`: `str` -> *optional*, default = `0.0.1`\n4. `conf_name`: `str` -> *optional*, default = `config` (filename of config file)\n5. `conf_ext`: `str` -> *optional*, default = `.json` (file extension for config file)\n6. `verbose`: `bool` -> *optional*, default = `False` (for verbose logging, needs more work)\n7. `defaults`: `dict` -> *optional*, no default value, can be used to set project default settings\n\n>Note: 2 and 3 not necessary, but may be used later for project config identification and things like version migration\n\n### Module functions\n\n```py\nfrom appconfig import AppConfig\n\nconfig = AppConfig(project_name="myProject")\n\nconfig.set(\'key\', \'value\')\nconfig.get(\'key\')\nconfig.get_all()\n```\n\n### To-do\n\n1. Atomically writing configs to prevent corruptions due to runtime errors or system crashes.\n2. A better validation system for config values. Right now it only makes sure it does not try to store a function.\n3. Type annotations. (partially done)\n\n\n## Related\n\nLoosely based on the same basic concept as some `npm` packages commonly used with javascript applications.\n- [`conf`](https://github.com/sindresorhus/conf) and [`appconfig`](https://raw.githubusercontent.com/anujdatar/appconfig).\n\n## License\n\n[MIT](https://github.com/anujdatar/py-appconfig/blob/master/LICENSE) Copyright (c) 2019-2021 Anuj Datar\n',
    'author': 'Anuj Datar',
    'author_email': 'anuj.datar@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/anujdatar/py-appconfig',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
