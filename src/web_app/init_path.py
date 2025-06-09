from pathlib import Path
from sys import path


app_root = Path(__file__).resolve().parent
project_root = str(app_root.parent)

if project_root not in path:
    path.append(project_root)


def cleanup_path():
    if project_root in path:
        path.remove(project_root)
