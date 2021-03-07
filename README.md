# Hasher - File hash generator written in Python
### Features
- Can calculate file hash for different algorithms at once.
- Memory/IO efficient. It reads file only once even when calculating hash for multiple algorithms.
- No other dependencies other than Python standard library.
- Supported algorithms. Supported algorithms depends on your Python version and OS.  
  To get the list of supported algorithms run `calc_hash.py -h`.

### Limitations
- All symbolic links will be ignored, support will be added in future.

### Install and run
There are multiple ways to run the hasher command line interface.
#### 1. Git clone and run `python -m hasher`
```
git clone https://github.com/random-user-00/hasher.git
python -m hasher -v
```
Only caveat is that you have to be in the parent directory of this repository or in the working directory.