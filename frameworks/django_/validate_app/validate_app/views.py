import ujson
from django.http import HttpResponse
from marshmallow import fields, Schema
from django.views.decorators.csrf import csrf_exempt


class SimpleSchema(Schema):

    name = fields.String()


SimpleSchema = SimpleSchema()


@csrf_exempt
def home(request):
    data, errors = SimpleSchema.load(ujson.loads(request.body))
    if not errors:
        return HttpResponse(content=ujson.dumps({'name': data['name']}))
