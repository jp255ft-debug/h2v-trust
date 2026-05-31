from pathlib import Path

root = Path('.')
ignore_dirs = {'.git', '__pycache__', 'node_modules', 'venv', '.next', 'cache', 'artifacts', 'build-info', 'test-next-app'}

def count_files(pattern):
    count = 0
    for f in root.rglob(pattern):
        if f.is_file() and not any(ig in str(f) for ig in ignore_dirs):
            count += 1
    return count

py = count_files('*.py')
ts = count_files('*.ts') + count_files('*.tsx')
sol = count_files('*.sol')
js = count_files('*.js')
md = count_files('*.md')
yml = count_files('*.yml') + count_files('*.yaml')
css = count_files('*.css')
docker = count_files('Dockerfile*')
json = count_files('*.json')
sh = count_files('*.sh')
cfg = count_files('*.ini') + count_files('*.cfg') + count_files('*.conf')

total_lines = 0
for ext in ['*.py', '*.ts', '*.tsx', '*.js', '*.sol', '*.css']:
    for f in root.rglob(ext):
        if f.is_file() and not any(ig in str(f) for ig in ignore_dirs):
            try:
                total_lines += len(f.read_text(encoding='utf-8', errors='ignore').splitlines())
            except:
                pass

print(f"Python: {py}")
print(f"TypeScript/TSX: {ts}")
print(f"Solidity: {sol}")
print(f"JavaScript: {js}")
print(f"Markdown: {md}")
print(f"YAML: {yml}")
print(f"CSS: {css}")
print(f"Dockerfiles: {docker}")
print(f"JSON: {json}")
print(f"Shell Scripts: {sh}")
print(f"Config: {cfg}")
print(f"Total de arquivos: {py+ts+sol+js+md+yml+css+docker+json+sh+cfg}")
print(f"Total de linhas de código: {total_lines}")
