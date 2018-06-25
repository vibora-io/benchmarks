#!/usr/bin/env python
import pycurl
from io import BytesIO
import time
import sys

url = sys.argv[1]
duration = float(sys.argv[2])
count = 0

print(f'URL: {url}')
c = pycurl.Curl()

start = now = time.time()

while (now - start < duration):
    bfr = BytesIO()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, bfr)
    c.perform()

    count += 1
    now = time.time()

print(f'  {count} requests in {now-start:.2f}s')
print(f'Requests/sec:{count / (now-start):10.2f}')
