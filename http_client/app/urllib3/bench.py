#!/usr/bin/env python
import urllib3
import time
import sys

url = sys.argv[1]
duration = float(sys.argv[2])
count = 0

print(f'URL: {url}')

start = now = time.time()

while (now - start < duration):
    session = urllib3.PoolManager()
    session.request('GET', url)
    count += 1
    now = time.time()

print(f'  {count} requests in {now-start:.2f}s')
print(f'Requests/sec:{count / (now-start):10.2f}')
