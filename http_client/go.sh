#!/bin/sh
# echo 10 > /proc/sys/net/ipv4/tcp_fin_timeout
# echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse
docker build -t bench .
docker run -it bench:latest
