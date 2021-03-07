import sys
from . import commandline

if __name__ == "__main__":
    print(sys.argv)
    print(sys.path)
    print(sys.exec_prefix)
    print(sys.flags)
    commandline.execute_command()
    