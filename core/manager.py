import os
import shutil
import subprocess
import time
from collections import defaultdict
from psutil import Process
from typing import List
from core.config import BenchmarkCategory, BenchmarkConfig, Framework
from vibora.utils import wait_server_offline, wait_server_available
from .utils import kill_recursively


class BenchmarkManager:

    def __init__(self, config: BenchmarkConfig):
        """

        :param config:
        """
        self.config = config
        self.frameworks: List[Framework] = config.enabled_frameworks
        self.categories: List[BenchmarkCategory] = config.categories

    def _run_benchmark(self, category: BenchmarkCategory):
        """

        :return:
        """
        config = self.config
        cmd = f'wrk -c 100 -t 4 http://{config.host}:{config.port}/ -d {config.wrk_duration}'
        if category.wrk_script:
            script_path = os.path.join(self.config.scripts_dir, category.wrk_script)
            cmd += f' -s {script_path}'
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait(config.wrk_duration + 2)
        return int(float(config.wrk_regex.search(p.stdout.read().decode()).groups()[0].strip()))

    def stop_server(self, pid: int, force: bool=True):
        """

        :param force:
        :param pid:
        :return:
        """
        kill_recursively(Process(pid), force=force)
        wait_server_offline(self.config.host, self.config.port)
        time.sleep(self.config.warm_up_time)

    def get_executable_path(self, framework: Framework):
        """

        :return:
        """
        new_path = os.path.join(self.config.virtualenvs_dir, framework.name.replace(' ', '_').lower())
        python_path = os.path.join(new_path, 'bin', 'python3')
        if not os.path.exists(new_path):
            p = subprocess.Popen(f'virtualenv -p python3.6 {new_path}', shell=True)
            p.wait(30)
            pip_path = os.path.join(os.path.dirname(python_path), 'pip')
            if framework.requirements:
                pip_ones = ' '.join((filter(lambda x: '/' not in x, framework.requirements)))
                if pip_ones:
                    p = subprocess.Popen(f'{pip_path} install --upgrade {pip_ones}', shell=True)
                    p.wait(60)
                for local_requirement in filter(lambda x: '/' in x, framework.requirements):
                    p = subprocess.Popen(f'{pip_path} install --upgrade {local_requirement}', shell=True)
                    p.wait(60)
        return python_path

    def benchmark_framework(self, script_path: str, framework: Framework, category: BenchmarkCategory):
        """

        :param category:
        :param script_path:
        :param framework:
        :return:
        """
        config = self.config
        python_path = self.get_executable_path(framework)
        p = subprocess.Popen([python_path, script_path, config.host, str(config.port)], stdout=subprocess.PIPE)
        try:
            wait_server_available(config.host, config.port)
            time.sleep(config.warm_up_time)
            return self._run_benchmark(category)
        except Exception as error:
            print(error)
            raise Exception(f'{script_path} failed to start (maybe something else) the server at '
                            f'{config.host}:{config.port} (Framework: {framework.name})')
        finally:
            self.stop_server(p.pid, framework.force_kill)

    def benchmark_all_frameworks(self):
        """

        :return:
        """
        scores = defaultdict(defaultdict)
        for framework in self.frameworks:
            framework_dir = os.path.join(self.config.frameworks_dir, framework.dirname)
            if os.path.exists(framework_dir):
                for category in self.categories:
                    script = os.path.join(framework_dir, category.filename)
                    if os.path.exists(script) and category.enabled:
                        for _ in range(0, self.config.rounds):
                            new_score = self.benchmark_framework(
                                script, framework=framework, category=category
                            )
                            if new_score > scores[category].get(framework.name, 0):
                                scores[category][framework.name] = new_score
            else:
                raise SystemExit(f"Missing dir {framework_dir} for framework: {framework.name}")
        return self.format_scores(scores)

    @staticmethod
    def format_scores(scores: defaultdict):
        new_scores = {}
        for category, value in scores.items():
            new_scores[category.name] = dict(value)
        return new_scores

    def clean(self):
        try:
            shutil.rmtree(self.config.virtualenvs_dir)
        except FileNotFoundError:
            pass
