#!/usr/bin/env python
import requests
import time
import sys

session = requests.Session()
url = sys.argv[1]
duration = float(sys.argv[2])
count = 0

print(f'URL: {url}')

start = now = time.time()

while (now - start < duration):
    session.get(url)
    count += 1
    now = time.time()

print(f'  {count} requests in {now-start:.2f}s')
print(f'Requests/sec:{count / (now-start):10.2f}')
