HTTP Client Benchmarks
======================

Run on an Intel Core i5 6300U (dual core skylake) in a docker container.

This isn't to get the "fastest" results, but a comparable result hence my choice of Apache2 as I could turn pipelining off so we can see if pipelining works correctly.
I kept each benchmark to a single process.


WRK is used as a baseline of what a top performer should be.

Results:
--------

SYNC              | Conn=1           | Pipelined Conn=1 
------------------|------------------|------------------
Requests          |           600.05 |           503.69 
Requests Opt      |           696.35 |           772.96 
urllib3           |          1318.85 |          1288.89 
urllib3 Opt       |          1515.80 |          1994.73 
PyCurl            |          4449.58 |          4518.28 
PyCurl Opt        |          5159.89 |         10255.08 

ASYNC             | Conn=1           | Conn=10          | Pipelined Conn=1 | Pipelined Conn=10
------------------|------------------|------------------|------------------|------------------
asks_trio         |           528.99 |           653.09 |           500.41 |           651.84 
asks_trio Opt     |           534.12 |           671.15 |          1201.38 |          1447.16 
aioHTTP           |           742.28 |          1050.93 |           455.42 |           976.85 
aioHTTP Opt       |           716.31 |          1136.30 |          1503.64 |          1768.74 
aioHTTP Opt UVloop|           985.65 |          1359.10 |          1631.60 |          2027.08 
vibora Opt        |          2255.25 |          3832.62 |           868.08 |          4160.42 

WRK               | Conn=1           | Conn=10          | Pipelined Conn=1 | Pipelined Conn=10
------------------|------------------|------------------|------------------|------------------
WRK Opt           |          5880.15 |         12793.40 |         15586.79 |         36713.39 

Usage:
------

On a system that has Docker, just run:
```sh
./go.sh
```
It should generate the result table for you.