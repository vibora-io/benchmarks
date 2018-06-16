import os
import re
from pathlib import Path
from typing import List
from vibora.utils import get_free_port


class Framework:
    def __init__(self, name: str, requirements: list=None, dirname: str=None,
                 enabled: bool=True, force_kill: bool=True):
        """

        :param name:
        :param requirements:
        :param dirname:
        """
        self.name = name
        self.requirements: List[str] = requirements or []
        self.dirname = dirname or self.name + '_'
        self.enabled = enabled
        self.force_kill = force_kill

    @classmethod
    def from_json(cls, config: dict):
        return cls(**config)

    def __repr__(self):
        return f'<{self.name}>'


class BenchmarkCategory:
    def __init__(self, name: str, filename: str, wrk_script: str=None, enabled: bool=True):
        """

        :param name:
        :param filename:
        :param wrk_script:
        """
        self.name = name
        self.filename = filename
        self.wrk_script = wrk_script
        self.enabled = enabled

    @classmethod
    def from_json(cls, config: dict):
        return cls(**config)


class BenchmarkConfig:

    def __init__(self, wrk_duration: int=30, rounds: int=1, warm_up_time: int=5,
                 host: str='127.0.0.1', port: int=None, frameworks: List[Framework]=None,
                 categories: List[BenchmarkCategory]=None,
                 virtualenvs_dir: str=None):
        """

        :param wrk_duration:
        :param rounds:
        :param warm_up_time:
        :param port:
        """
        self.frameworks_dir = os.path.join(Path(__file__).parents[1], 'frameworks')
        self.scripts_dir = os.path.join(Path(__file__).parents[1], 'wrk_scripts')
        self.host = host or '127.0.0.1'
        self.port = port or get_free_port(self.host)[2]
        self.wrk_duration = wrk_duration
        self.rounds = rounds
        self.warm_up_time = warm_up_time
        self.frameworks: List[Framework] = frameworks or []
        self.categories: List[BenchmarkCategory] = categories or []
        self.wrk_regex = re.compile('Requests/sec: (.*?)\\n')
        self.virtualenvs_dir = virtualenvs_dir or os.path.join(os.path.dirname(__file__), '.venvs')

    def get_category(self, filename: str=None, name: str=None):
        for c in self.categories:
            if c.filename == filename or c.name == name:
                return c

    @property
    def enabled_frameworks(self) -> list:
        return list(filter(lambda f: f.enabled, self.frameworks))

    @classmethod
    def from_json(cls, config: dict) -> 'BenchmarkConfig':
        objects = {'categories': BenchmarkCategory, 'frameworks': Framework}
        for object_name, object_type in objects.items():
            temp = []
            for item in config.get(object_name, []):
                temp.append(object_type.from_json(item))
            config[object_name] = temp
        return cls(**config)
