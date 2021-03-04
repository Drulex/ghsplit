import argparse
import logging
import sys

from .ghsplit import find_files_to_split, find_files_to_merge, split, merge


logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Manipulate large files to avoid exceeding Github quotas",
        add_help=False,
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

    subparsers = parser.add_subparsers(
        help='the command; type "ghsplit COMMAND -h" for command-specific help',
        dest='command',
    )

    split_parser = subparsers.add_parser("split", help="Split large files into chunks")

    split_parser.add_argument("--chunk-size",
        type=int,
        default=50,
        help="Chunk size (in MiB). Default=50",
    )

    split_parser.add_argument("--max-size",
        type=int,
        default=99,
        help="Max size of file before splitting (in MiB). Default=99",
    )

    split_parser.add_argument("--extension",
        type=str,
        help="Only consider files with a specific extension (e.g. '.bin')",
    )

    def do_split(args):
        to_split = find_files_to_split(max_size_MiB=args.max_size, root=args.root, ext=args.extension)
        if not to_split:
            parser.error("Did not find any large file to split!")
        done = split(files=to_split, chunk_MiB=args.chunk_size)
        for x in done:
            logger.info("Created chunk %s!", x)

    split_parser.set_defaults(func=do_split)

    merge_parser = subparsers.add_parser("merge", help="Merge chunks into large files")

    def do_merge(args):
        to_merge = find_files_to_merge(root=args.root)
        if not to_merge:
            parser.error("Did not find any chunk files to merge!")
        merged = merge(files=to_merge)
        for x in merged:
            logger.info("Merged %s from chunks", x)

    merge_parser.set_defaults(func=do_merge)

    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except:
        pass

    args = parser.parse_args()

    logging.basicConfig(
     datefmt="%Y-%m-%dT%H:%M:%S",
     level=getattr(logging, args.log_level),
     format="%(asctime)-15s %(name)s %(levelname)s %(message)s"
    )

    if getattr(args, 'func', None) is None:
        parser.print_help()
        return 1
    else:
        return args.func(args)


if __name__ == '__main__':
    raise SystemExit(main())