# ####################################################################
# HTTP Client benchmarks
# This isn't to get the "fastest" results, but a comparable result
#  hence my choice of Apache2 as I could turn pipelining off
#  so we can see if pipelining works correctly.
# ####################################################################
FROM python:3.6-alpine3.7
WORKDIR /app/

# Install and set-up run-time dependancies
RUN apk add --no-cache tini wrk apache2 libcurl openssl && \
    mkdir /run/apache2

# Install build-time dependencies, builds requirements, then unintsall build-time dependencies
# This is done in one step, so as to not require squashing
RUN apk add --no-cache gcc musl-dev make curl-dev openssl-dev g++ && \
    pip install urllib3 requests pycurl aiohttp cchardet aiodns uvloop trio asks vibora && \
    apk del --purge gcc musl-dev make curl-dev openssl-dev g++

# Install custom code & config files
COPY app/ /app/

# Entrypoint with zombie reaper
CMD ["/sbin/tini", "--", "/app/entrypoint.sh"]
