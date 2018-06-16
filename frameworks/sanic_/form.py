import sys
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from multiprocessing import cpu_count


app = Sanic()


@app.route('/', methods=['POST'])
async def home(request: Request):
    return json({'count': len(request.files)})


if __name__ == '__main__':
    app.run(host=sys.argv[1], port=int(sys.argv[2]), debug=False, workers=cpu_count(), access_log=False)