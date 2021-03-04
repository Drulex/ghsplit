#!/usr/bin/env python

import logging
import argparse
import sys
import io
import os
from pathlib import Path
from typing import Sequence


logger = logging.getLogger(__name__)

SIZE_LIMIT_B = 99 * 1024 * 1024

def get_parser():

    parser = argparse.ArgumentParser(
        description="Manipulate large files to avoid exceeding Github quotas",
        add_help=False,
    )

    action = parser.add_mutually_exclusive_group()

    action.add_argument(
        "-split",
        action="store_true",
        help="Automatically split files exceeding github's quota (do this before commit/push!)"
    )

    action.add_argument(
        "-merge",
        action="store_true",
        help="Automatically merge split files (do this after fetching/pulling!)"
    )

    parser.add_argument("-h", "--help", action="help",
        help="show this help message and exit"
    )

    parser.add_argument("--log-level",
        default="INFO",
        help="Logging level (eg. INFO, see Python logging docs)",
    )

    parser.add_argument("--root",
        type=str,
        help="Root dir to look for large files (recursively). $CWD if None.",
    )

    parser.add_argument("--chunk-size",
        type=int,
        default=50,
        help="Chunk size (in MiB). Default=50",
    )

    return parser


def find_files_to_split(root=None):
    if root is None:
        root = Path().absolute() # cwd

    to_split = []

    # todo pass suffix as arg?
    for f in Path(root).glob('**/*.nii.gz'):
        if f.stat().st_size > SIZE_LIMIT_B:
            to_split.append(f)

    return to_split

def find_files_to_merge(root=None):
    if root is None:
        root = Path().absolute() # cwd

    # will do for now
    return [f for f in Path(root).glob('**/*.ghsplit.*')]


def split(files: Sequence[Path], chunk_MiB):
    """
    For each large file split it in chunks of size=size.
    Save it as ${filename}.ghslit_XX where XX is a numerical suffix.
    """
    size_b = chunk_MiB * 1024 * 1024
    to_commit = []

    for file in files:
        logger.info("Splitting file %s", file)
        fsize = file.stat().st_size
        chunks = (fsize // size_b) + 1
        with io.open(file, 'rb') as fi:
            for idx in range(chunks):
                chunk_data = fi.read(size_b)
                chunk_name = "{}.ghsplit.{:02}".format(file.name, idx)
                chunk_path = file.with_name(chunk_name)
                with io.open(chunk_path, 'wb') as fo:
                    logger.debug("writing chunk %s", chunk_path)
                    fo.write(chunk_data)
                    to_commit.append(chunk_path)

        os.remove(file)

    return to_commit


def merge(files: Sequence[Path]):
    """
    """
    merged = []
    groups = dict()

    # create groups of chunks corresponding to the appropriate file
    for file in files:
        filename = file.name.split(".ghsplit")[0]
        chunks = groups.get(filename, [])
        chunks.append(file)
        groups[filename] = chunks

    for filename, chunks in groups.items():
        file_path = chunks[0].with_name(filename)
        logger.info("Merging %s", file_path)
        with io.open(file_path, 'wb') as fo:
            for chunk in sorted(chunks):
                logger.debug("Processed chunk %s", chunk.name)
                with io.open(chunk, 'rb') as fi:
                    fo.write(fi.read())

                os.remove(chunk)
        merged.append(file_path)

    return merged


def main():
    parser = get_parser()
    args = parser.parse_args()

    logging.basicConfig(stream=sys.stdout, level=args.log_level,
                        format="%(levelname)s %(message)s")

    logger.debug("args=%s", args)

    if args.split:
        to_split = find_files_to_split(root=args.root)
        if not to_split:
            parser.error("Did not find any large file to split!")
        done = split(files=to_split, chunk_MiB=args.chunk_size)
        for x in done:
            print("Don't forget to commit {}!".format(x))

    elif args.merge:
        to_merge = find_files_to_merge(root=args.root)
        if not to_merge:
            parser.error("Did not find any chunk files to merge!")
        merged = merge(files=to_merge)
        for x in merged:
            print("Merged {} from chunks".format(x))


if __name__ == '__main__':
    raise SystemExit(main())
