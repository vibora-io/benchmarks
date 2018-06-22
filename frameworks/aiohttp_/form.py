import os
import sys
import subprocess
import ujson
from aiohttp import web
from multiprocessing import cpu_count
# from aiohttp.web_request import FileField


async def hello(request):
    values = await request.post()
    # Aiohttp doesn't provide a shortcut to access the files only (streaming function must be slower)
    # so we gonna give a hand and just count any parameter.
    # return web.Response(text=ujson.dumps({'count': len(list(filter(
    #     lambda x: isinstance(x, FileField), values.values()
    # )))}))
    return web.Response(text=ujson.dumps({'count': len(values.values())}))


app = web.Application()
app.add_routes([web.post('/', hello)])


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)
    gunicorn_path = os.path.join(os.path.dirname(sys.executable), 'gunicorn')
    cmd = f'{gunicorn_path} form:app -w {cpu_count()} ' \
          f'--worker-class="aiohttp.worker.GunicornUVLoopWebWorker" -b {sys.argv[1]}:{sys.argv[2]}'
    p = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
