#!/usr/bin/env python

import logging
import io
import os
from pathlib import Path
from typing import Sequence


logger = logging.getLogger(__name__)


def find_files_to_split(max_size_MiB: int, root: str=None, ext: str=None):
    if root is None:
        root = Path().absolute() # cwd
    else:
        root = Path(root)

    to_split = []

    if ext is not None:
        glob_pattern = "**/*{}".format(ext)
    else:
        glob_pattern = "**/*"

    for f in Path(root).glob(glob_pattern):
        if ".ghsplit" in f.name:
            continue
        if f.stat().st_size > (max_size_MiB * 1024 * 1024):
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
