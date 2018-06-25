#!/usr/bin/env python
import re
import sys

val = sys.stdin.read()

vals = [text.strip() for text in val.strip().split('\n\n')]

groups = {}

for bench in vals:
    desc = bench.split('\n')[0]
    group = desc.split(':')[0].strip()
    app = desc.split(':')[1].strip()
    pipelined = 'Pipelined' if 'Pipelined' in desc else ''
    opt = ' Opt' if 'Opt' in desc else ''
    uvloop = ' UVloop' if 'UVloop' in desc else ''
    cons = re.search(r'Concurrency:(\d+)', desc).group(1)
    reqs = re.search(r'\nRequests/sec:\s*([\d\.]+)', bench).group(1)
    spec = f'{app}{opt}{uvloop}'
    subspec = f'{pipelined} Conn={cons}'.strip()
    groups.setdefault(group, {}).setdefault(spec, {})[subspec] = reqs

for gname, group in groups.items():
    _subspecs = set()
    for sname, spec in group.items():
        _subspecs.update(list(spec.keys()))
    subspecs = sorted(_subspecs)

    cols = ""
    cold = ""
    for col in subspecs:
        cols += f"| {col:17}"
        cold += f"|{'-'*18}"
    print(f'\n{gname:18}{cols}')
    print(f"{'-'*18}{cold}")
    for sname, spec in group.items():
        cols = ""
        for col in subspecs:
            cols += f"|{spec.get(col,''):>17} "
        print(f'{sname:18}{cols}')
