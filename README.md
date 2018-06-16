### Python Web Benchmarks

A simple project to benchmark Python web frameworks against [Vibora](http://vibora.io) in
a few use cases (more cases will be added soon).

### Running Instructions

1. Install Docker (sudo apt-get install docker.io)

2. Clone the project (git clone https://github.com/vibora-io/benchmarks)

3. Build the image (sudo docker build . -t vibora_benchmarks)

4. Run the benchmark (sudo docker run vibora_benchmarks)

> You can configure the benchmark by editing config.json.

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

### Results (AWS c5.2xlarge - 8 CPU cores - Dedicated Tenancy)

-------------
#### Infamous Hello World
> Testing how fast they can answer a static response. Not much useful but it sets the high bar for each framework.

> Sanic does not send the "Date" http header which is a violation of the HTTP protocol (actually you could argue that this header is not mandatory but since it's used every where by cache engines (and the RFC says unless you don't have a clock you must send) I wouldn't even lose my time arguing).
-------------

| Frameworks    | Requests/Sec  | Version |
| ------------- |:-------------:|:-------:|
| Tornado       | 14,249         | 5.02    |
| Django        | 22,727         | 2.0.6   |
| Flask         | 37,139         | 1.0.2   |
| Aiohttp       | 40,86          | 3.3.2   |
| Sanic         | 116,195        | 0.7.0   |
| Vibora        | 361,685        | 0.0.6   |

-------------
#### Validate JSON
> Testing how fast they receive a JSON, parse and validate it. Frameworks that do not have a validation engine (or it's too slow) are using Marshmallow, at least for now, unless a fast and tested library appears on the wild.

> Vibora/Aiohttp have "streaming enabled" by default which means the user can receive the response in chunks (or even reject it) before sending the response... So beware that Sanic, for example, has a streaming mode which makes the route slower than normal and could affect performance.
-------------

| Frameworks    | Requests/Sec  | Version |
| ------------- |:-------------:|:-------:|
| Tornado       | 12,159         | 5.02    |
| Flask         | 18,216         | 1.0.2   |
| Django        | 18,364         | 2.0.6   |
| Aiohttp       | 26,204         | 3.3.2   |
| Sanic         | 70,284         | 0.7.0   |
| Vibora        | 131,292        | 0.0.6   |


-------------
#### Forms Parsing
> Testing how fast they receive (and parse) a POST with a multipart-form inside it containing a few parameters and one single file.

> Most frameworks with the exception of Vibora and Aiohttp do not have a streaming multipart parser which means they must load the entire form in-memory (big file uploads are impracticable) before letting the user interact with it (unless of course you read the stream yourself and parse it).
-------------

| Frameworks    | Requests/Sec  | Version |
| ------------- |:-------------:|:-------:|
| Aiohttp       | 2,229         | 3.3.2   |
| Django        | 7,294         | 2.0.6   |
| Tornado       | 10,199        | 5.02    |
| Flask         | 11,858        | 1.0.2   |
| Sanic         | 46,516        | 0.7.0   |
| Vibora        | 76,524        | 0.0.6   |

-------------
#### Redis API
> Testing how fast they receive a POST with a JSON, validate it and do a simple GET in Redis.
-------------

| Frameworks    | Requests/Sec  | Version |
| ------------- |:-------------:|:-------:|
| Tornado       | 12,159        | 5.02    |
| Flask         | 18,216        | 1.0.2   |
| Django        | 18,364        | 2.0.6   |
| Aiohttp       | 26,242        | 3.3.2   |
| Sanic         | 70,284        | 0.7.0   |
| Vibora        | 131,292       | 0.0.6   |

