
import pathlib
import sys

from . import dmap
from . import dotrender
from . import settings


if __name__ == '__main__':
    assert len(sys.argv) == 2
    root = sys.argv[1]
    assert root

    root = pathlib.Path(root).resolve()
    if not root.is_dir():
        raise RuntimeError("The path '{}' is not a directory!".format(str(root)))

    fs = dmap.map_directory(root, count_files=settings.COUNT_FILES)

    rendering = dotrender.dotrender(fs)
    dotrender.dotexport(root.name, rendering)
    dotrender.dotopen(root.name)
