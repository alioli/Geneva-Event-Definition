from pathlib import Path

src = Path('.github/scripts/run_restructure_corrected.py').read_text()
old = "src = Path('.github/scripts/restructure_lower_locality.py').read_text()"
new = """import subprocess
src = subprocess.check_output([
    'git', 'show',
    '5d4b09756978fa79f63c7c069277d4da9bd37136:.github/scripts/restructure_lower_locality.py'
], text=True)"""
if old not in src:
    raise SystemExit('corrected runner source hook not found')
src = src.replace(old, new, 1)
exec(compile(src, '.github/scripts/run_restructure_corrected.py', 'exec'), {'__name__': '__main__'})
