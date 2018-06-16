import ujson
import redis
from django.http import HttpResponse
from marshmallow import fields, Schema
from django.views.decorators.csrf import csrf_exempt

r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set('1', 'hello world')


class SimpleSchema(Schema):

    key_name = fields.String()


SimpleSchema = SimpleSchema()


@csrf_exempt
def home(request):
    data, errors = SimpleSchema.load(ujson.loads(request.body))
    if not errors:
        return HttpResponse(content=r.get(data['key_name']))
