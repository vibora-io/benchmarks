import sys
import os
import subprocess
from multiprocessing import cpu_count
from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/', methods=['POST'])
def home():
    return jsonify({'count': len(request.files)}), 200


if __name__ == '__main__':
    cwd = os.path.dirname(__file__)
    gunicorn_path = os.path.join(os.path.dirname(sys.executable), 'gunicorn')
    cmd = f'{gunicorn_path} form:app -w {cpu_count()} ' \
          f'--worker-class="egg:meinheld#gunicorn_worker" -b {sys.argv[1]}:{sys.argv[2]}'
    p = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
