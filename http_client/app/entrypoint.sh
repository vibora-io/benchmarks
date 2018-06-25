#!/bin/sh
set -e

# Configure Apache2
echo "ServerName 127.0.0.1:80" >> /etc/apache2/httpd.conf
sed -i 's/^LoadModule log_config_module .*$//g' /etc/apache2/httpd.conf
sed -i 's/^LoadModule mpm_prefork_module .*$//g' /etc/apache2/httpd.conf
sed -i 's/^#LoadModule mpm_worker_module/LoadModule mpm_worker_module/g' /etc/apache2/httpd.conf
# Launch Apache2
httpd -k start
sleep 2

echo '' > /app/out

export URL=http://127.0.0.1/index.html
export DURATION=2
export PAUSE=4

export CONS=1
sleep $PAUSE
DESC='Pipelined, Concurrency:1' /app/benchmarks.sh

export CONS=10
sleep $PAUSE
DESC='Pipelined, Concurrency:10' /app/benchmarks.sh

# Configure Apache2 to force disale pipelining
sed -i 's/^KeepAlive On$/KeepAlive Off/g' /etc/apache2/conf.d/default.conf
# Restart Apache2
httpd -k restart
export PAUSE=15

export CONS=1
sleep $PAUSE
DESC='No Pipelining, Concurrency:1' /app/benchmarks.sh

export CONS=10
sleep $PAUSE
DESC='No Pipelining, Concurrency:10' /app/benchmarks.sh

# Print report to screen
cat /app/out | ./present.py
