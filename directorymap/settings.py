
import sys
assert sys.version_info >= (3, 4, 0)
import pathlib


# paths
ROOT = pathlib.Path(__file__).resolve().parent
OUTPUT_FOLDER = ROOT / "renders"

# mapping
COUNT_FILES = True

IGNORE_CONTENTS = frozenset([
    '.git',
    'lib',
    'bin',
    'include',
])

DONT_SHOW = frozenset([
])

# rendering
COLOR_SATURATION = 0.333
