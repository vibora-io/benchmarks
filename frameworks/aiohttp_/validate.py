import os
import sys
import subprocess
import aioredis
from aiohttp import web
from multiprocessing import cpu_count
from marshmallow import Schema, fields

app = web.Application()


class SimpleSchema(Schema):

    name = fields.String()


SimpleSchema = SimpleSchema()


async def hello(request):
    values = await request.json()
    data, errors = SimpleSchema.load(values)
    if not errors:
        return web.Response(body=data['name'].encode())


app.add_routes([web.post('/', hello)])


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)
    gunicorn_path = os.path.join(os.path.dirname(sys.executable), 'gunicorn')
    cmd = f'{gunicorn_path} validate:app -w {cpu_count()} ' \
          f'--worker-class="aiohttp.worker.GunicornUVLoopWebWorker" -b {sys.argv[1]}:{sys.argv[2]}'
    p = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
