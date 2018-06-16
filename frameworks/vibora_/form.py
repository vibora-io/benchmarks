import sys
from multiprocessing import cpu_count
from vibora import Vibora, Request
from vibora.responses import JsonResponse


app = Vibora(template_dirs=['/tmp/asd'])


@app.route('/', methods=['POST'], cache=False)
async def home(request: Request):
    return JsonResponse({'count': len(await request.files())})


if __name__ == '__main__':
    app.run(host=sys.argv[1], workers=cpu_count(), debug=False, port=int(sys.argv[2]))
