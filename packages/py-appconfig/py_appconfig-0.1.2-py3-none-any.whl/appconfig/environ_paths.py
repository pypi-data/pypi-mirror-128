from tempfile import gettempdir
from os import getenv
from pathlib import Path
import sys
from typing import Dict

home_dir = Path.home()
temp_dir = Path(gettempdir())


def mac_paths(name: str) -> Dict:
    """
    :param name:
    :return: paths for data/logs/config/temp, etc
    """
    library = home_dir / 'Library'
    return {
        "data": library / 'Application Support' / name,
        "config": library / 'Preferences' / name,
        "cache": library / 'Caches' / name,
        "log": library / 'Logs' / name,
        "temp": temp_dir / name
    }


def win_paths(name: str) -> Dict:
    """
    windows is not opinionated, you can use any locations
    :param name:
    :return: paths for data/logs/config/temp, etc
    """
    app_data = Path(getenv("APPDATA") or home_dir / 'AppData' / 'Roaming')
    local_app_data = Path(getenv("LOCALAPPDATA") or home_dir / 'AppData' / 'Local')

    return {
        "data": local_app_data / name / 'Data',
        "config": app_data / name / 'Config',
        "cache": local_app_data / name / 'Cache',
        "log": local_app_data / name / 'Log',
        "temp": temp_dir / name
    }


def linux_paths(name: str) -> Dict:
    """
    using xdg-basedir spec
    :param name:
    :return:
    """
    data_home = Path(getenv("XDG_DATA_HOME") or home_dir / '.local' / 'share')
    config_home = Path(getenv("XDG_CONFIG_HOME") or home_dir / '.config')
    cache_home = Path(getenv("XDG_CACHE_HOME") or home_dir / '.cache')
    log_home = Path(getenv("XDG_STATE_HOME") or home_dir / '.local' / 'state')

    return {
        "data": data_home / name,
        "config": config_home / name,
        "cache": cache_home / name,
        "log": log_home / name,
        "temp": temp_dir / name
    }


def env_paths(name: str) -> Dict:
    """
    define env_paths based on the detected platform
    :param name:
    :return:
    """
    platform = sys.platform

    if platform == 'darwin':
        return mac_paths(name)
    if platform == 'win32':
        return win_paths(name)
    return linux_paths(name)


if __name__ == '__main__':
    print(env_paths('test'))
