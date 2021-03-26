"""
File hash generator written in Python. Supports generating hash for multiple algorithms at same time.
Usage example
>>> import hasher.filehasher
>>> hash = hasher.filehasher.generate("/tmp/file1", "md5")
>>> hash
{'/tmp/file1': {'md5': '0d5ea07883d0ccff5c9dedf79f9e6631'}}
>>> 
>>> multiple_hashes = hasher.filehasher.generate("/tmp/file1", "md5", "sha1")
>>> multiple_hashes
{'/tmp/file1': {'md5': '0d5ea07883d0ccff5c9dedf79f9e6631', 'sha1': '28da374cfe95d44bd19e1b7ddb699288a9edefa2'}}
>>> 

Supported hash algorithms
>>> hasher.shared.SUPPORTED_HASH
{'sha3_384', 'sha512_224', 'sha3_224', 'sha384', 'sm3', 'md5', 'shake_256', 'ripemd160', 'whirlpool', 'sha3_256', 'sha256', 'sha512', 'md5-sha1', 'mdc2', 'sha224', 'shake_128', 'sha512_256', 'blake2b', 'sha3_512', 'sha1', 'blake2s', 'md4'}
>>> 
"""

__version__ = "1.0.dev1"
