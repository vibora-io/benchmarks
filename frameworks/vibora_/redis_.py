import sys
import aioredis
from multiprocessing import cpu_count
from aioredis.commands import Redis
from vibora import Vibora, Response, Request
from vibora.hooks import Events
from vibora.schemas import Schema


app = Vibora()


class SimpleSchema(Schema):

    key_name: str


@app.handle(Events.BEFORE_SERVER_START)
async def before_start():
    redis = await aioredis.create_redis('redis://localhost')
    await redis.set('1', 'hello world')
    app.components.add(redis)


@app.route('/', methods=['POST'])
async def home(request: Request, redis: Redis):
    schema = await SimpleSchema.load_json(request)
    value = await redis.get(schema.key_name)
    return Response(value)


if __name__ == '__main__':
    app.run(host=sys.argv[1], workers=cpu_count(), debug=False, port=int(sys.argv[2]))
