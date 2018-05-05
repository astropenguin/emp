# coding: utf-8

"""Empower your Mac with simple scripts.

Usage:
  emp <action> <path> [options]
  emp -h | --help
  emp -v | --version

Options:
  -h --help             Show the help and exit.
  -v --version          Show the version and exit.
  -f --force            Force to answer every question with Yes.
  --pattern <pattern>   Name pattern of empfiles [default: *empfile*.yaml].
  --github <user/repo>  Clone a empfiles' repository from GitHub.
  --gitlab <user/repo>  Clone a empfiles' repository from GitLab.
  --url <url>           Clone a empfiles' repository from a URL.
  --log <filename>      Output log to a file instead of stdout.

"""

from __future__ import absolute_import, print_function, unicode_literals

# standard library
import os
import re
import sys
from logging import basicConfig

# dependent packages
import emp
from docopt import docopt


# functions
def clone(args):
    if args['--github']:
        return emp.clone_from_github(args['--github'])
    elif args['--gitlab']:
        return emp.clone_from_gitlab(args['--gitlab'])
    elif args['--url']:
        return emp.clone_from_url(args['--url'])


def main():
    args = docopt(__doc__, version=emp.__version__)
    # logging
    # clone
    # os.walk
    # prompt


# main
if __name__ == '__main__':
    main()
