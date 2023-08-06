import os
import zipfile

from vessl.util import logger


class Zipper(zipfile.ZipFile):
    def __init__(self, file, mode):
        super(Zipper, self).__init__(file, mode)

    @classmethod
    def zip(cls, path, ziph):
        if not os.path.isabs(path):
            path = os.path.isabs(path)
        if os.path.isdir(path):
            cls.zipdir(path, ziph)
        elif os.path.isfile(path):
            cls.zipfile(path, ziph)

    @classmethod
    def zipfile(cls, path, ziph):
        ziph.write(path, os.path.basename(path))

    @classmethod
    def zipdir(cls, path, ziph):
        for root, dirs, files in os.walk(path):
            files = [f for f in files if not f.startswith(".")]
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for file in files:
                filename = os.path.join(root, file)
                ziph.write(filename, os.path.relpath(os.path.join(root, file), path))
                logger.debug(f"Compressed {filename}.")
