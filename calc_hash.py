#!/usr/bin/python
import os
import io
import argparse
import pathlib
import hashlib
import stat

def file_hash(file_path, *hash_algos):
    hash_objects = {}
#    if hash_algo not in {hashlib.algorithms_available}:
#        print(f'Unknown hash algorithm {hash_algo}')
#        return -1
    for algo in hash_algos:
        hash_objects[algo] = hashlib.new(algo)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        buffer_size = io.DEFAULT_BUFFER_SIZE
        read_size = buffer_size
        with open(file_path, 'rb', buffering=buffer_size) as _f:
            content = _f.read(read_size)
#            reads = 1
#            hash_generator_md5 = hashlib.md5()
#            hash_generator_sha256 = hashlib.sha256()
# According to Python documentation named constructors are faster than new(),
# but then with named constrctors it will be harder to create constructors based on user arguments.
#            hash_generator_md5 = hashlib.new('md5')
#            hash_generator_sha256 = hashlib.new('sha256')
            while content:
                for algo in hash_objects:
                    hash_objects[algo].update(content)
#                hash_generator_md5.update(content)
#                hash_generator_sha256.update(content)
                content = _f.read(read_size)
#                reads += 1             
#            print(hash_generator_md5.hexdigest(), hash_generator_sha256.hexdigest())
            for _hash, _value in hash_objects.items():
                print(file_path, _hash, type(_value), _value.name, _value.hexdigest())
#            print(f'Total reads {reads}')

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
            file_hash(file, *args.hash_algo)
        else:
            print(f'file {file} not found')

 
