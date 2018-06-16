import os
import json
import pprint
import subprocess
from core.manager import BenchmarkManager, BenchmarkConfig


if __name__ == '__main__':

    # Starting Redis server.
    p = subprocess.Popen('/usr/bin/redis-server', shell=True)

    # Loading configs.
    root = os.path.join(os.path.dirname(__file__))
    with open(os.path.join(root, 'config.json')) as f:
        config = BenchmarkConfig.from_json(json.load(f))

    # Displaying benchmark configs
    each_framework = config.wrk_duration + config.warm_up_time * 2
    total_time = config.rounds * each_framework * (len(config.enabled_frameworks) * len(config.categories))
    print(f'Benchmarking: {", ".join([x.name for x in config.enabled_frameworks])}')
    print('===' * 50)
    print(f'Please be patient. This benchmark will take at least {round(total_time / 60, 1)} minutes to run. \n'
          f'(Lowering the wrk_time, rounds, categories configs help if you are in a hurry)')
    print('===' * 50)

    # Running the benchmark.
    manager = BenchmarkManager(config)
    manager.clean()
    scores = manager.benchmark_all_frameworks()
    print('===' * 50)
    pprint.pprint(scores)

    # Stopping redis.
    p.terminate()
