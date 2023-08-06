import hashlib
from typing import IO
from pathlib import Path

BLOCKSIZE = 65536


def hash_file(path: Path) -> str:

    with path.open("rb") as file_:
        return hash_stream(file_)


def hash_stream(stream: IO[bytes]) -> str:
    hasher = hashlib.md5()
    buffer = stream.read(BLOCKSIZE)
    while len(buffer) > 0:
        hasher.update(buffer)
        buffer = stream.read(BLOCKSIZE)
    return hasher.hexdigest()
