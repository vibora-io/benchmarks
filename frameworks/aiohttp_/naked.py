import os
import sys
import subprocess
from aiohttp import web
from multiprocessing import cpu_count


async def hello(request):
    return web.Response(text="Hello, world")


app = web.Application()
app.add_routes([web.get('/', hello)])


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)
    gunicorn_path = os.path.join(os.path.dirname(sys.executable), 'gunicorn')
    cmd = f'{gunicorn_path} naked:app -w {cpu_count()} ' \
          f'--worker-class="aiohttp.worker.GunicornWebWorker" -b {sys.argv[1]}:{sys.argv[2]}'
    p = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
