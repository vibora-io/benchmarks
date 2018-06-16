### Python Web Benchmarks

Benchmarks the most famous Python web frameworks against Vibora in
a few use cases.

### Running Instructions

1. Install Docker (sudo apt-get install docker.io)

2. Clone the project and build the image. (git clone https://github.com/vibora-io/benchmarks && sudo docker build . -t vibora_benchmarks)

3. Run the container (sudo docker run vibora_benchmarks)

### Disclaimer

- Benchmarks are more of a sport than science, don't make assumptions, do your own benchmarks.

- There are one zillion more important things to consider when choosing
a framework. Be wise.

- I tried to "optimize" each framework but I'm not
an expert in every single one.

- This benchmark mixes sync/async frameworks so to make up a "fair" fight
there is no latency between database requests. Async frameworks under
high concurrency and high latency databases would
perform much better than sync ones thanks to the architecture.

- Talking about concurrency: WRK is configured to 100 concurrent
users which is pretty low number, again, to make it fair against
sync frameworks.

- Users of WSGI are configured to use Gunicorn + Meinheld which
is the fastest option although not the most stable one.

### Results (AWS c5.2xlarge - 8 CPU cores)