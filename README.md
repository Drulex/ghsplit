# ghsplit

Automatically split and merge large files so that they don't exceed Github's quota.

## Installation
```
pip install --user -e .

# alternatively
make install
```

## Testing
```
make test
```

## Usage

Simply use `ghsplit split` before pushing and `ghsplit merge` after pulling.

```
$ python ghsplit.py -h
usage: ghsplit [-h] [--log-level LOG_LEVEL] [--root ROOT] {split,merge} ...

Manipulate large files to avoid exceeding Github quotas

positional arguments:
  {split,merge}         the command; type "ghsplit COMMAND -h" for command-
                        specific help
    split               Split large files into chunks
    merge               Merge chunks into large files

optional arguments:
  -h, --help            show this help message and exit
  --log-level LOG_LEVEL
                        Logging level (eg. INFO, see Python logging docs)
  --root ROOT           Root dir to look for large files (recursively). $CWD
                        if None.
```

Splitting has some options available:
```
usage: ghsplit split [-h] [--chunk-size CHUNK_SIZE] [--max-size MAX_SIZE]
                     [--extension EXTENSION]

optional arguments:
  -h, --help            show this help message and exit
  --chunk-size CHUNK_SIZE
                        Chunk size (in MiB). Default=50
  --max-size MAX_SIZE   Max size of file before splitting (in MiB). Default=99
  --extension EXTENSION
                        Only consider files with a specific extension (e.g.
                        '.bin')
```

### Splitting examples
```
# split all files in current working dir that are greater than 99Mib in chunks of 50MiB (GH compatible)
$ ghsplit split

# split only niftii files greater than 25MiB in the template directory in chunks of 5MiB
$ ghsplit --root=template split --max-size=25 --extension=.nii.gz --chunk-size=5

```

### Merging example
```
# you can always safely run this to merge all splitted files
$ ghsplit merge
```

