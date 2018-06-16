import sys
import aioredis
from multiprocessing import cpu_count
from sanic import Sanic
from sanic.request import Request
from sanic.response import text
from marshmallow import Schema, fields

app = Sanic(__name__)
redis = None


class SimpleSchema(Schema):

    key_name = fields.String()


SimpleSchema = SimpleSchema()


@app.listener('after_server_start')
async def after_server_start(app, loop):
    global redis
    redis = await aioredis.create_redis('redis://localhost', loop=loop)
    await redis.set('1', 'hello world')


@app.route('/', methods=['POST'])
async def home(request: Request):
    data, errors = SimpleSchema.load(request.json)
    if not errors:
        value = await redis.get(data['key_name'])
        return text(value.decode())


if __name__ == '__main__':
    app.run(host=sys.argv[1], port=int(sys.argv[2]), debug=False, workers=cpu_count(), access_log=False)
