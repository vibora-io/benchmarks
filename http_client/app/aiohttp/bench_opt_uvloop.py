#!/usr/bin/env python
import aiohttp
import asyncio
import time
import sys
from typing import Tuple
import uvloop

url = sys.argv[1]
duration = float(sys.argv[2])
concurrency = int(sys.argv[3])

print(f'URL: {url}')

async def worker() -> Tuple[int, float]:
    count = 0
    start = now = time.time()
    async with aiohttp.ClientSession() as session:
        while (now - start < duration):
            async with session.get(url) as resp:
                await resp.read()
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

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()
loop.run_until_complete(bench())

