#!/usr/bin/env python3

"""
Directory mapper
"""

import json
import os
import pathlib

from . import filestructure
from . import settings


FILES_KEY = "files"
DIRECTORIES_KEY = "directories"


def parse_directory_keys(path):
    keys = path.parts
    if '/' in keys[:1]:
        keys = keys[1:]
    return keys


def map_directory(root, count_files=True):
    walker = os.walk(str(root))

    # file_structure = table()
    file_structure = filestructure.FileStructure(count_files=count_files)

    for (dirpath, dirnames, filenames) in walker:
        path = pathlib.Path(dirpath)
        last = path.parts[-1]
        if last in settings.IGNORE_CONTENTS | settings.DONT_SHOW:
            del dirnames[:]
        if last in settings.DONT_SHOW:
            continue

        if count_files:
            filenames = len(filenames)

        keys = parse_directory_keys(path)
        fobj = file_structure.get(keys)
        fobj.set_files(filenames)

    return file_structure


def pprint(directory):
    print(json.dumps(directory.to_dict(), indent=4))
