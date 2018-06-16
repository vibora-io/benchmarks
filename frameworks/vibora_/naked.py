import sys
from multiprocessing import cpu_count
from vibora import Vibora, Response

app = Vibora()


@app.route('/')
async def home():
    return Response(b'Naked!')


if __name__ == '__main__':
    app.run(host=sys.argv[1], workers=cpu_count(), debug=False, port=int(sys.argv[2]))
