"""Create the comparison map fixtures; run with CHECKOUT SUPPORT_DIR arguments."""
from pathlib import Path
import shutil
import sys
import zipfile

checkout, support = map(Path, sys.argv[1:])
fixtures = Path(__file__).parent
for mod, source, name in [
    ('ts', 'sunstroke', 'radar-building'),
    ('ra', 'a-path-beyond.oramap', 'radar-ra'),
    ('d2k', 'pasty-mesa', 'radar-d2k'),
    ('cnc', 'african-gambit.oramap', 'radar-cnc'),
]:
    src = checkout / 'mods' / mod / 'maps' / source
    dest = support / 'maps' / mod / '{DEV_VERSION}' / name
    dest.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
        shutil.copytree(src, dest, dirs_exist_ok=True)
    else:
        with zipfile.ZipFile(src) as archive:
            archive.extractall(dest)
    shutil.copy2(fixtures / (name + '.yaml'), dest / 'map.yaml')
    print(mod, name, dest)
