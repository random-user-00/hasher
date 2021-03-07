# This is just workaround so that users can run `python -m hasher`
# instead of `python -m hasher.hasher` from directory of cloned git repository

from .hasher import commandline

if __name__ == "__main__":
    commandline.execute_command()
