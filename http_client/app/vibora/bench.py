#!/usr/bin/env python
from vibora import client
import asyncio
import time
import sys
from typing import Tuple

url = sys.argv[1]
duration = float(sys.argv[2])
concurrency = int(sys.argv[3])

print(f'URL: {url}')

async def worker() -> Tuple[int, float]:
    count = 0
    start = now = time.time()
    while (now - start < duration):
        await client.get(url)
        count += 1
        now = time.time()

    return count, now - start

async def bench():
    tasks = []
    for val in range(concurrency):
        tasks.append(asyncio.ensure_future(worker()))
    count = 0
    duration = 0.0
    for task in tasks:
        await task
        res = task.result()
        count += res[0]
        duration += res[1]

    print(f'  {count} requests in {duration / concurrency:.2f}s')
    print(f'Requests/sec:{count / (duration / concurrency):10.2f}')

loop = asyncio.get_event_loop()
loop.run_until_complete(bench())

