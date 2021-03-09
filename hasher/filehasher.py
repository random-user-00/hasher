#!/usr/bin/python
import os
import io
import pathlib
import hashlib
from . import shared

def generate(file_path, hash_algo, *hash_algos):
    """Takes a single path like object/path string and a single algorithm name/tuple 
    of algorithm names or  as argument and returns a dictionary of calculated hashes.
    e.g. generate("userpaths", "md5", "sha256")
    { userpaths: {"md5": "md5 hash", "sha256": "sha256 hash},...}
    >>> 
    >>> import calc_hash
    >>> calc_hash.generate("~/Downloads/chrome-linux.zip", "md5", "sha1")
    {'/home/tejas/Downloads/chrome-linux.zip': {'md5': '3d9d23669bd49f2bf5d92b076f4428c8', 'sha1': '64c73a9fe00079a828bdd04ec42aa2f2410991a3'}}
    >>> 
    """
    # os.path.expanduser(path) will expand the path if it starts with ~ 
    # If path doesn't contain ~ it will be returned unchanged. 
    path_expanded = os.path.expanduser(file_path)

    # If script is run as command, argument file_path is always of type PosixPath.
    # If function is called from another module, argument file_path can be a string or path like object.
    # To be consistent, let's store it as string. This string_path will serve as key in returned dictionary.
    path_as_str = str(pathlib.Path(path_expanded).resolve(strict=True))
    hash_algos =  (hash_algo,) + hash_algos
    hash_objects = {}
    hash_hex = {path_as_str: {}}
    # named constructors are faster than new(), but usint it would be harder
    # to create constructors based on user arguments.
    for algo in hash_algos:
        if algo not in shared.SUPPORTED_HASH:
            raise ValueError(f'Unknown hash type {algo!r}, known types: {shared.SUPPORTED_HASH}')
        hash_objects[algo] = hashlib.new(algo)

    if os.path.exists(path_as_str) and os.path.isfile(path_as_str):
        buffer_size = io.DEFAULT_BUFFER_SIZE
        read_size = io.DEFAULT_BUFFER_SIZE
        with open(path_as_str, 'rb', buffering=buffer_size) as _f:
            content = _f.read(read_size)
            while content:
                for algo in hash_objects:
                    hash_objects[algo].update(content)
                content = _f.read(read_size)
            for _hash, _value in hash_objects.items():
                hash_hex[path_as_str][_value.name] = _value.hexdigest()         
            return hash_hex
def validate():
    """Validate user input before passing it to generate().

    """
    pass
