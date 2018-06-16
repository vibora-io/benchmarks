import sys
import os
import redis
import subprocess
from flask import Flask
from flask import request
from multiprocessing import cpu_count
from marshmallow import Schema, fields


app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set('1', 'hello world')


class SimpleSchema(Schema):

    key_name = fields.String()


SimpleSchema = SimpleSchema()


@app.route('/')
def home():
    data, errors = SimpleSchema.load(request.json)
    if not errors:
        value = r.get(data['key_name'])
        return value, 200


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)
    gunicorn_path = os.path.join(os.path.dirname(sys.executable), 'gunicorn')
    cmd = f'{gunicorn_path} naked:app -w {cpu_count()} ' \
          f'--worker-class="egg:meinheld#gunicorn_worker" -b {sys.argv[1]}:{sys.argv[2]}'
    p = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
