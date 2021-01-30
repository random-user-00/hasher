#!/usr/bin/python
import os
import io
import argparse
import pathlib
import hashlib
import stat

def file_hash(file_path):
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
            hash_generator_md5 = hashlib.new('md5')
            hash_generator_sha256 = hashlib.new('sha256')
            while content:
                hash_generator_md5.update(content)
                hash_generator_sha256.update(content)
                content = _f.read(read_size)
#                reads += 1             
            print(hash_generator_md5.hexdigest(), hash_generator_sha256.hexdigest())
#            print(f'Total reads {reads}')

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Provide file path and hash algorithm to calculate file hash")
    parser.add_argument(dest="filepath", type=pathlib.Path, metavar="filepath", help="Filename/Path")
    parser.add_argument(dest="hash_algo", type=str, metavar="hash_algo",choices=hashlib.algorithms_available, help="Suppprted algorithms:  %(choices)s")
    args = parser.parse_args()
#    print(args)
    if args.filepath.exists():
#        print('file exists')
        file_hash(args.filepath)
    else:
        print(f'file {args.filepath} not found')


