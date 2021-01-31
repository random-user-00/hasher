#!/usr/bin/python
import os
import io
import argparse
import pathlib
import hashlib
import stat
import sys

def generate(file_path, hash_algo, *hash_algos):
    """ Takes a path like object and a list of hash algorithms as argument and
    return a dictionary of calculated hashes.
    { filepath: {"md5": "md5 hash", "sha256": "sha256 hash},...}
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
#    if hash_algo not in {hashlib.algorithms_available}:
#        print(f'Unknown hash algorithm {hash_algo}')
#        return -1
    for algo in hash_algos:
        if algo not in hashlib.algorithms_available:
            raise ValueError(f'Unknown hash type {algo!r}, known types: {hashlib.algorithms_available}')
        hash_objects[algo] = hashlib.new(algo)

    if os.path.exists(path_as_str) and os.path.isfile(path_as_str):
        buffer_size = io.DEFAULT_BUFFER_SIZE * 2
        read_size = buffer_size
        with open(path_as_str, 'rb', buffering=buffer_size) as _f:
            content = _f.read(read_size)
#            reads = 1
#            hash_generator_sha256 = hashlib.sha256()
# According to Python documentation named constructors are faster than new(),
# but then with named constrctors it will be harder to create constructors based on user arguments.
#            hash_generator_sha256 = hashlib.new('sha256')
            while content:
                for algo in hash_objects:
                    hash_objects[algo].update(content)
#                hash_generator_sha256.update(content)
                content = _f.read(read_size)
#                reads += 1             
            for _hash, _value in hash_objects.items():
#                print(file_path, _value.name, _value.hexdigest())
                hash_hex[path_as_str][_value.name] = _value.hexdigest()         
#            print(hash_hex, sys.getsizeof(hash_hex))
#            print(f'Total reads {reads}')
            return hash_hex


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Provide file path(s) and "
                                     "hash algorithm(s) to calculate file hash")
    parser.add_argument("-f", "--file", dest="filepath", nargs='+',
                        type=pathlib.Path, required=True , help="file path")
    parser.add_argument("-a", "--algo", dest="hash_algo", type=str, nargs='+',
                        metavar="hash_algorithm",
                        choices=hashlib.algorithms_available, required=True,
                        help="Suppprted algorithms:  %(choices)s")
    args = parser.parse_args()
    hash_tuple = tuple(args.hash_algo)
    filepaths = []
    for file in args.filepath:
        if file.exists():
            filepaths.append(file)
#            print(file, hash_tuple)
            hash = generate(file, *args.hash_algo)
            print(hash)
        else:
            print(f'file {file} not found')

 
