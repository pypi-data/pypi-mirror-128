"""
Python package template with command-line interface
"""

import argparse
from . import __version__


def cli_args():
    """Define & examine command-line arguments & options."""
    _desc = f"{__package__}: " + __doc__.strip().splitlines()[0]
    p = argparse.ArgumentParser(description=_desc)
    p.add_argument("-v", "--version", action="version", version=__version__)
    return p.parse_args()


def main():
    # simple function of this package, return a string
    # args = cli_args()  # FIXME: fails in CI
    return f"{__name__} {__version__ = } of {__file__ = }"


if __name__ == "__main__":
    main()
