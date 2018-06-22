import os
import sys
import subprocess
import aioredis
from aiohttp import web
from multiprocessing import cpu_count
from marshmallow import Schema, fields

app = web.Application()


class SimpleSchema(Schema):

    key_name = fields.String()


async def create_redis(current_app):
    redis = await aioredis.create_redis('redis://localhost')
    await redis.set('1', 'hello world')
    current_app['redis'] = redis


SimpleSchema = SimpleSchema()


async def hello(request):
    values = await request.json()
    data, errors = SimpleSchema.load(values)
    if not errors:
        value = await app['redis'].get(data['key_name'])
        return web.Response(body=value)


app.add_routes([web.post('/', hello)])
app.on_startup.append(create_redis)


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)
    gunicorn_path = os.path.join(os.path.dirname(sys.executable), 'gunicorn')
    cmd = f'{gunicorn_path} redis_:app -w {cpu_count()} ' \
          f'--worker-class="aiohttp.worker.GunicornUVLoopWebWorker" -b {sys.argv[1]}:{sys.argv[2]}'
    p = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
