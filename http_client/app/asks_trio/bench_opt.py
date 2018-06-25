#!/usr/bin/env python
import asks
import trio
import time
import sys
from typing import List, Tuple
asks.init('trio')

url = sys.argv[1]
duration = float(sys.argv[2])
concurrency = int(sys.argv[3])

print(f'URL: {url}')

async def worker(tasks: List[Tuple[int, float]]) -> None:
    count = 0
    start = now = time.time()
    s = asks.Session()
    while (now - start < duration):
        await s.get(url)
        count += 1
        now = time.time()

    tasks.append((count, now - start))

async def bench():
    tasks = []
    async with trio.open_nursery() as nursery:
        for val in range(concurrency):
            nursery.start_soon(worker, tasks)

    count = 0
    duration = 0.0
    for task in tasks:
        count += task[0]
        duration += task[1]

    print(f'  {count} requests in {duration / concurrency:.2f}s')
    print(f'Requests/sec:{count / (duration / concurrency):10.2f}')


trio.run(bench)

