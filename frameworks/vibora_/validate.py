import sys
from vibora import Vibora, Request, cpu_count
from vibora.responses import JsonResponse
from vibora.schemas import Schema


class SimpleSchema(Schema):

    name: str


app = Vibora()


@app.route('/', methods=['POST'])
async def home(request: Request):
    schema = await SimpleSchema.load_json(request)
    return JsonResponse({'name': schema.name})


if __name__ == '__main__':
    app.run(host=sys.argv[1], port=int(sys.argv[2]), debug=False, workers=cpu_count())
