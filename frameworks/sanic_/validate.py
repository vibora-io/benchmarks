import sys
from marshmallow import Schema, fields
from multiprocessing import cpu_count
from sanic import Sanic
from sanic.request import Request
from sanic.response import json


class SimpleSchema(Schema):

    name = fields.String()


SimpleSchema = SimpleSchema()

app = Sanic(__name__)


@app.route('/', methods=['POST'])
async def home(request: Request):
    data, errors = SimpleSchema.load(request.json)
    return json({'name': data['name']})


if __name__ == '__main__':
    app.run(host=sys.argv[1], port=int(sys.argv[2]), debug=False, workers=cpu_count(), access_log=False)
