#!/usr/bin/python
import os
import io
import argparse
import pathlib
import hashlib
import queue

def generate(file_path, hash_algo, *hash_algos):
    """ Takes a path like object or path string and a list of hash algorithms as argument and
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

    for algo in hash_algos:
        if algo not in hashlib.algorithms_available:
            raise ValueError(f'Unknown hash type {algo!r}, known types: {hashlib.algorithms_available}')
        hash_objects[algo] = hashlib.new(algo)

    if os.path.exists(path_as_str) and os.path.isfile(path_as_str):
        buffer_size = io.DEFAULT_BUFFER_SIZE
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
def validate():
    """Validate user input before passing it to generate().

    """
    pass

if __name__ == "__main__":
    formatter_class = argparse.RawDescriptionHelpFormatter
    description = ("Provide -f file path(s) and -a hash algorithm(s) to calculate \n"
                     "file hash. Accepts single file/directory or space-separated \n"
                     "list of files/directories. Accepts single algorithm or \n"
                     "space-seperated list of algorithms.")
    description_new ='''
        Provide -f file path(s) and -a hash algorithm(s) to calculate file hash.
        Accepts single file/directory or space-separated list of files/directories.
        Accepts single algorithm or space-seperated list of algorithms.
        '''
    parser = argparse.ArgumentParser(description=description_new, formatter_class=formatter_class)
    parser.add_argument("-f", "--file", dest="filepath", nargs='+',
                        type=pathlib.Path, required=True , help="file/directory path(s)")
    parser.add_argument("-a", "--algo", dest="hash_algo", type=str, nargs='+',
                        metavar="hash_algorithm",
                        choices=hashlib.algorithms_available, required=True,
                        help="Suppprted algorithms:  %(choices)s")
    parser.add_argument("-r", "--recurse", dest="recurse",
                        default=False, action="store_true",
                        required=False,
                        help="Recursively scan subdirectories for files if -f is directory")
    args = parser.parse_args()
    hash_tuple = tuple(args.hash_algo)
    filepaths = []
    dirpaths = queue.Queue()
    print(args.filepath)
    print(args.recurse)
    for file in args.filepath:
        if (file.exists() and file.is_file()) and not file.is_symlink():
            filepaths.append(file)
#            print(file, hash_tuple)
            hash = generate(file, *args.hash_algo)
            print(hash)
        elif (file.exists() and file.is_dir()) and not file.is_symlink():
            dirpaths.put(file.resolve())   
        else:
            print(f'file/dir path {file} not found or it is a symbolic link.')
    
    while not dirpaths.empty():
        subpath = dirpaths.get()
        for _file in subpath.iterdir():
            if (_file.exists() and _file.is_dir()) and not _file.is_symlink():
                dirpaths.put(_file)
            elif (_file.exists() and _file.is_file()) and not _file.is_symlink():
                hash2 = generate(_file, *args.hash_algo)
                print(hash2)
            else:
                print(f'file/dir path {_file} not found or it is a symbolic link.')