"""
Recursive file structure object
"""


import collections


class FileStructure(object):
    """Represents a folder"""

    REGISTRY = collections.defaultdict(dict)

    def __init__(self, name="", path="n0", count_files=True):
        key = path.count('_')
        FileStructure.REGISTRY[key]
        assert path not in FileStructure.REGISTRY[key]
        FileStructure.REGISTRY[key][path] = self

        self.path = path
        self.children = 0

        self.name = name
        self.count_files = count_files
        self.files = 0 if count_files else []
        self.directories = {}

    def next_child_path(self):
        self.children += 1
        return "{}_{}".format(self.path, self.children - 1)

    def get(self, keys):
        assert keys
        (key, *rest) = keys
        if not rest:
            return self[key]
        else:
            return self[key].get(rest)

    def set_files(self, files):
        self.files = files

    def num_files(self):
        return self.files if self.count_files else len(self.files)

    def __getitem__(self, key):
        if key not in self.directories:
            fs = FileStructure(key, self.next_child_path(), count_files=self.count_files)
            self.directories[key] = fs
        return self.directories[key]

    def to_dict(self):
        data = {
            "name": self.name,
            "path": self.path,
            "files": self.files,
        }

        if self.directories:
            data.update({"directories": {k: v.to_dict() for (k, v) in self.directories.items()}})

        return data

    def __repr__(self):
        return "<FileStructure: {}, {}, {}>".format(self.path, self.name, self.children)
