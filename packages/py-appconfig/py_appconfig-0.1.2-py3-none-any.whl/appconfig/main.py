from pathlib import Path
import json
from typing import Any, Dict
from appconfig import env_paths


def value_type_check(value: Any) -> None:
    """Just ensures a function is not passed"""
    _acceptable = [str, int, float, complex, dict, list, tuple, bool, type(None)]
    if type(value) not in _acceptable:
        print('value is of type: ', type(value))
        raise ValueError


class AppConfig:
    """
    app config object for a python app
    :param:
        kwargs: project_name (String) -> mandatory
                conf_name (String) -> optional, default = config
                conf_ext (String) -> optional, default = .json
                verbose (Boolean) -> optional, default = False
    :return: persistent config file for project in default config location
    """

    def __init__(self, **kwargs):
        super().__init__()

        # get all kwargs passed to class constructor
        self.project_name = kwargs['project_name']
        self.project_id = kwargs.get('project_id', self.project_name)
        self.project_version = kwargs.get('version', '0.0.1')
        self.conf_name = kwargs.get('conf_name', 'config')
        self.conf_ext = kwargs.get('conf_ext', '.json')
        self.verbose = kwargs.get('verbose', False)
        self.defaults = kwargs.get('defaults', None)
        self.config = dict()

        self.conf_file = self.conf_name + self.conf_ext
        self.config_folder = env_paths(self.project_name)['config']
        self.config_path = self.config_folder / self.conf_file
        self.temp_conf = self.config_folder / 'tmpfile'
        self.verbose_log('Config Path: ', self.config_path)

        self.verbose_log('Checking of config_file exists')
        if not Path(self.config_folder).is_dir():
            # if config folder does not already exist
            self.first_init()
        else:
            if Path(self.config_path).is_file():
                self.verbose_log('check existing config file is valid json')
                if not self.validate_config_file_integrity():
                    self.verbose_log('existing config not valid json, resetting to default config')
                    self.first_init()

        self.config = self.get_all()

    def create_empty_json_file(self) -> None:
        """create a valid empty json file at config path"""
        with open(self.config_path, 'w') as f:
            json.dump({}, f)

    def first_init(self) -> None:
        """create config folder+file when none exist at first init"""
        Path.mkdir(self.config_folder, parents=True, exist_ok=True)
        Path.touch(self.config_path)
        self.create_empty_json_file()

        self.config['projectName'] = self.project_name
        self.config['projectId'] = self.project_id
        self.config['version'] = self.project_version
        self.set_defaults()

    def set_defaults(self) -> None:
        if isinstance(self.defaults, dict):
            for (key, value) in self.defaults.items():
                self.config[key] = value
            self.write_conf()

    def validate_config_file_integrity(self) -> bool:
        """verify if config file is valid json"""
        with open(self.config_path, 'r') as f:
            _data = f.read()
        try:
            _config = json.loads(_data)
            self.verbose_log('Config file exists and is valid JSON')
            return True
        except json.JSONDecodeError:
            self.verbose_log('Invalid config file, replacing with base config')
            # self.first_init()
            return False

    def get_all(self) -> Dict:
        """get all values stored in config file"""
        with open(self.config_path) as f:
            return json.load(f)

    def get(self, key: str) -> Any:
        """get single config value from config store"""
        try:
            return self.config[key]
        except KeyError:
            self.verbose_log('Invalid key')
            return

    def set(self, key: str, value: Any) -> None:
        """set value of configuration in store"""
        # validate key data type
        if type(key) != str:
            raise KeyError
        # validate value data type
        value_type_check(value)
        self.config[key] = value

        # write config to file
        self.write_conf()

    def reset_all(self) -> None:
        self.config = dict()
        self.first_init()

    def reset(self, key: str) -> None:
        if key in self.defaults:
            self.verbose_log(f'resetting {key} config to default value')
            __default_value = self.defaults[key]
            self.config[key] = __default_value
            self.write_conf()
        else:
            self.verbose_log(f'{key} has no default value, deleting entry corresponding to {key}')
            self.delete(key)

    def delete(self, key: str) -> None:
        if key in self.config:
            self.verbose_log(f'deleting {key} config')
            del self.config[key]
            self.write_conf()
        else:
            self.verbose_log(f'{key} has no set config, doing nothing')

    def verbose_log(self, *args) -> None:
        """print statements if you want a verbose run for debug"""
        if self.verbose:
            print(*args)

    def write_conf(self) -> None:
        # TODO make writing file atomic
        # check 'http://stupidpythonideas.blogspot.com/2014/07/getting-atomic-writes-right.html'
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f)
