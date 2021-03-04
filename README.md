# ghsplit

Automatically split and merge large files so that they don't exceed Github's quota.

## Usage

Simply use `ghsplit.py -split` before pushing and `ghsplit -merge` after pulling.

```
$ python ghsplit.py -h
usage: ghsplit.py [-split | -merge] [-h] [--log-level LOG_LEVEL] [--root ROOT]
                  [--chunk-size CHUNK_SIZE]

Manipulate large files to avoid exceeding Github quotas

optional arguments:
  -split                Automatically split files exceeding github's quota (do
                        this before commit/push!)
  -merge                Automatically merge split files (do this after
                        fetching/pulling!)
  -h, --help            show this help message and exit
  --log-level LOG_LEVEL
                        Logging level (eg. INFO, see Python logging docs)
  --root ROOT           Root dir to look for large files (recursively). $CWD
                        if None.
  --chunk-size CHUNK_SIZE
                        Chunk size (in MiB). Default=50
```

### Prior to pushing
```
$ ls -lh big_files_directory/
total 233M
-rw-r--r-- 1 drulex drulex 233M Mar  4 11:33 bigfile1.nii.gz

$ md5sum big_files_directory/*
138a2dc926d2616e96df6a433043f750  big_files_directory/bigfile1.nii.gz

$ python ghsplit.py --root big_files_directory/ -split
INFO Splitting file big_files_directory/bigfile1.nii.gz
Don't forget to commit big_files_directory/bigfile1.nii.gz.ghsplit.00!
Don't forget to commit big_files_directory/bigfile1.nii.gz.ghsplit.01!
Don't forget to commit big_files_directory/bigfile1.nii.gz.ghsplit.02!
Don't forget to commit big_files_directory/bigfile1.nii.gz.ghsplit.03!
Don't forget to commit big_files_directory/bigfile1.nii.gz.ghsplit.04!

$ ls -lh big_files_directory/
total 233M
-rw-r--r-- 1 drulex drulex 50M Mar  4 11:34 bigfile1.nii.gz.ghsplit.00
-rw-r--r-- 1 drulex drulex 50M Mar  4 11:34 bigfile1.nii.gz.ghsplit.01
-rw-r--r-- 1 drulex drulex 50M Mar  4 11:34 bigfile1.nii.gz.ghsplit.02
-rw-r--r-- 1 drulex drulex 50M Mar  4 11:34 bigfile1.nii.gz.ghsplit.03
-rw-r--r-- 1 drulex drulex 33M Mar  4 11:34 bigfile1.nii.gz.ghsplit.04

$ git add big_files_directory/*.ghsplit.*

$ git commit -m "Added bigfile1.nii.gz"
[master 44331d4] Added bigfile1.nii.gz
 5 files changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 big_files_directory/bigfile1.nii.gz.ghsplit.00
 create mode 100644 big_files_directory/bigfile1.nii.gz.ghsplit.01
 create mode 100644 big_files_directory/bigfile1.nii.gz.ghsplit.02
 create mode 100644 big_files_directory/bigfile1.nii.gz.ghsplit.03
 create mode 100644 big_files_directory/bigfile1.nii.gz.ghsplit.04

$ git push origin ...
```

### After pulling
```
$ python ghsplit.py --root big_files_directory/ -merge
INFO Merging big_files_directory/bigfile1.nii.gz
Merged big_files_directory/bigfile1.nii.gz from chunks

$ ls -lh big_files_directory/
total 233M
-rw-r--r-- 1 drulex drulex 233M Mar  4 11:35 bigfile1.nii.gz

$ md5sum big_files_directory/*
138a2dc926d2616e96df6a433043f750  big_files_directory/bigfile1.nii.gz

```

