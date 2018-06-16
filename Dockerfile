FROM ubuntu:18.04

ENV ROOT_DIR /pybenchmarks
ENV PYTHON /virtualenv/bin/python
ENV PIP /virtualenv/bin/pip

RUN apt-get update
RUN apt-get install -y software-properties-common git virtualenv unzip build-essential python3.6-dev libssl-dev

# Installing WRK (benchmark tool)
RUN git clone https://github.com/wg/wrk.git /tmp/wrk
WORKDIR /tmp/wrk
RUN make -j4
RUN cp /tmp/wrk/wrk /usr/local/bin

# Installing redis
RUN apt-get install -y redis-server

# Creating a virtualenv and installing required libraries.
ADD . ${ROOT_DIR}
RUN virtualenv -p python3.6 /virtualenv
RUN ${PIP} install -r ${ROOT_DIR}/requirements.txt

CMD ${PYTHON} ${ROOT_DIR}/run.py