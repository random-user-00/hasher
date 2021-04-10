import queue
import pathlib

from . import arghandler
from . import filehasher

def commandline(args):
    path_q: queue.Queue[pathlib.Path] = queue.Queue()
    for _userpath in args.userpaths:  # -f arguments to queue
        if (_userpath.exists() and not _userpath.is_symlink()) and _userpath.is_dir():
            path_q.put(_userpath)
        elif (_userpath.exists() and not _userpath.is_symlink()) and _userpath.is_file():
            try:
                _hash1 = filehasher.generate(_userpath, *args.hash_algo)  # Unpack args.hash_algo
                print(_hash1)
            except PermissionError:
                print(f'No permission to read {_userpath}')
        else:
            print(f'info:1 file/dir path {_userpath} not found or it is a symbolic link.')

    while not path_q.empty():
        path: pathlib.Path = path_q.get()         
        child: pathlib.Path
        try:
            for child in path.iterdir():
                if (child.exists() and child.is_dir()) and not child.is_symlink():
                    if args.recurse:
                        path_q.put(child)
                elif (child.exists() and child.is_file()) and not child.is_symlink():
                    try:
                        _hash = filehasher.generate(child, *args.hash_algo)  # Unpack args.hash_algo
                        print(_hash)
                    except PermissionError:
                        print(f'Exception: PermissionError: No permission to read {child}')
                else:
                    print(f'info:2 file/dir path {child} not found or it is a symbolic link.')
        except PermissionError:
            print(f'Exception: PermissionError: No permission to read directory {path}')




def execute_command():
    _get_args = arghandler.process_args()
    args = _get_args.parse_args()
    commandline(args)
