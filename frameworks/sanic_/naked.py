import sys
from multiprocessing import cpu_count
from sanic import Sanic
from sanic.request import Request
from sanic.response import raw

app = Sanic(__name__)


@app.route('/')
async def home(request: Request):
    return raw(b'Naked!')


if __name__ == '__main__':
    app.run(host=sys.argv[1], port=int(sys.argv[2]), debug=False, workers=cpu_count(), access_log=False)
