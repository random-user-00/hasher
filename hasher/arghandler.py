import argparse
import pathlib

from . import shared

def process_args():
    formatter = argparse.RawDescriptionHelpFormatter
    descr = """
Description:
    Provide -f file/dir path(s) and -a hash algorithm(s) to calculate file hash.
    Accepts single file/directory or space-separated list of files/directories.
    Accepts single algorithm or space-seperated list of algorithms.
    Use -r if you wish to recursively scan directory."""

    _usage = """
    hasher -f file/dir -a hash-algorithm [-r] [-v] [-h]
    Run hasher -h/--help for detailed help
usage example:
     hasher -f /tmp/file1 -a sha256
    or if you are running as Python module
     python -m hasher /tmp/file1 -a sha256
     """

    _prog_name = shared.PROG_NAME
    parser = argparse.ArgumentParser(description=descr, formatter_class=formatter,
                    prog=_prog_name, add_help=False, usage=_usage)

    required_args = parser.add_argument_group("Required Arguments")
    _f_help = "file/directory path(s), accepts space-separated list of file/dir."
    required_args.add_argument("-f", "--file", dest="userpaths", nargs='+',
                    metavar="file/dir", type=pathlib.Path, required=True,
                    help=_f_help)
    _a_choices = shared.SUPPORTED_HASH
    _a_help = """hash algorithm(s), accepts single or space separated list of
              hash function names. Suppprted hash functions:  %(choices)s"""
    required_args.add_argument("-a", "--algo", dest="hash_algo", type=str, nargs='+',
                    metavar="hash-algorithm",
                    choices=_a_choices, required=True, help=_a_help)
    
    optional_args = parser.add_argument_group("Optional Arguments")
    _r_help = "Recursively scan subdirectories for files if -f is directory"
    optional_args.add_argument("-r", "--recurse", dest="recurse",
                    default=False, action="store_true",
                    required=False, help=_r_help)
    optional_args.add_argument("-v", "--version", action="version",
                    version=f'{_prog_name} {shared.__version__}',
                    help="Display version")
    optional_args.add_argument("-h", "--help", action="help",
                    help="Display this help message")
    return parser
