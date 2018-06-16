import sys
import os
import subprocess
from multiprocessing import cpu_count


if __name__ == '__main__':
    cwd = os.path.join(os.path.dirname(__file__), 'form_app')
    gunicorn_path = os.path.join(os.path.dirname(sys.executable), 'gunicorn')
    cmd = f'{gunicorn_path} form_app.wsgi:application -w {cpu_count()} ' \
          f'--worker-class="egg:meinheld#gunicorn_worker" -b {sys.argv[1]}:{sys.argv[2]}'
    p = subprocess.Popen(cmd, shell=True, cwd=cwd)
    p.wait()
