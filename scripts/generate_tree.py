import os, sys

exclude_dirs = {'node_modules', 'venv', '__pycache__', '.pytest_cache', '.next', '.git', '.vscode', 'Lib', 'Scripts', 'share', 'include'}
exclude_ext = {'.pyc', '.pyo'}
exclude_files = {'tree_completo.txt', 'tree_clean.txt', 'package-lock.json'}

def walk(path, prefix=''):
    items = sorted(os.listdir(path))
    dirs = [d for d in items if os.path.isdir(os.path.join(path, d)) and d not in exclude_dirs]
    files = [f for f in items if os.path.isfile(os.path.join(path, f)) and os.path.splitext(f)[1] not in exclude_ext and f not in exclude_files]
    
    for i, item in enumerate(dirs + files):
        is_last = (i == len(dirs) + len(files) - 1)
        connector = '|__ ' if is_last else '|-- '
        print(f'{prefix}{connector}{item}')
        
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            extension = '    ' if is_last else '|   '
            walk(full_path, prefix + extension)

sys.stdout.reconfigure(encoding='utf-8')
print('h2v-trust/')
walk('.')
