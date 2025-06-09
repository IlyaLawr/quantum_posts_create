from subprocess import Popen
from pathlib import Path
from sys import executable

from shared_module.db_utils import create_table
from shared_module.settings import settings

project_root = Path(__file__).resolve().parent

tg_app_path = project_root / 'tg_app'
web_app_path = project_root / 'web_app'


def run_apps():
    tg_process = Popen([executable, 
                        'tg_app.py'],
                        cwd=tg_app_path)

    web_process = Popen([executable,
                        '-m', 'uvicorn',
                        'web_app:app',
                        '--host', settings.web_app_host,
                        '--port', settings.web_app_port,
                        '--reload'],
                        cwd=web_app_path)

    try:
        web_process.wait()
        tg_process.wait()
    except KeyboardInterrupt:
        tg_process.terminate()
        web_process.terminate()


if __name__ == '__main__':
    create_table()
    run_apps()
