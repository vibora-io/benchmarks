#!/bin/sh

if [ "X$CONS" == "X1" ]; then
# Requests
echo SYNC: Requests: $DESC | tee -a /app/out
/app/requests/bench.py $URL $DURATION | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

echo SYNC: Requests: Opt $DESC | tee -a /app/out
/app/requests/bench_session.py $URL $DURATION | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE


# urllib3
echo SYNC: urllib3: $DESC | tee -a /app/out
/app/urllib3/bench.py $URL $DURATION | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

echo SYNC: urllib3: Opt $DESC | tee -a /app/out
/app/urllib3/bench_session.py $URL $DURATION | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE


# PyCurl
echo SYNC: PyCurl: $DESC | tee -a /app/out
/app/pycurl/bench.py $URL $DURATION | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

echo SYNC: PyCurl: Opt $DESC | tee -a /app/out
/app/pycurl/bench_session.py $URL $DURATION | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE
fi

# asks_trio
echo ASYNC: asks_trio: $DESC | tee -a /app/out
/app/asks_trio/bench.py $URL $DURATION $CONS | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

echo ASYNC: asks_trio: Opt $DESC | tee -a /app/out
/app/asks_trio/bench_opt.py $URL $DURATION $CONS | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

# aioHTTP
echo ASYNC: aioHTTP: $DESC | tee -a /app/out
/app/aiohttp/bench.py $URL $DURATION $CONS | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

echo ASYNC: aioHTTP: Opt $DESC | tee -a /app/out
/app/aiohttp/bench_opt.py $URL $DURATION $CONS | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

echo ASYNC: aioHTTP: Opt UVloop $DESC | tee -a /app/out
/app/aiohttp/bench_opt_uvloop.py $URL $DURATION $CONS | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

# Vibora
echo ASYNC: vibora: Opt $DESC | tee -a /app/out
/app/vibora/bench.py $URL $DURATION $CONS | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

# Tornado
echo ASYNC: Tornado.simple: $DESC | tee -a /app/out
/app/tornado/bench.py $URL $DURATION $CONS | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

echo ASYNC: Tornado.simple: UVloop $DESC | tee -a /app/out
/app/tornado/bench_uvloop.py $URL $DURATION $CONS | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

echo ASYNC: Tornado.curl: $DESC | tee -a /app/out
/app/tornado/bench_curl.py $URL $DURATION $CONS | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

echo ASYNC: Tornado.curl: UVloop $DESC | tee -a /app/out
/app/tornado/bench_curl_uvloop.py $URL $DURATION $CONS | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE

# WRK
echo WRK: WRK: Opt $DESC | tee -a /app/out
wrk -d ${DURATION}s -t 1 -c $CONS $URL | tee -a /app/out
echo | tee -a /app/out
sleep $PAUSE
