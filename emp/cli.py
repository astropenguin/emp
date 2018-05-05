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
def set_logging(args):
    basicConfig(filename=args['--log'], filemode='w',
                datefmt='%Y-%m-%d %H:%M:%S',
                format='%(asctime)s | %(levelname)-8s | %(message)s')

    logger.setLevel(INFO)


def clone_repo(args):
    if args['--github']:
        repo = emp.clone_from_github(args['--github'])
    elif args['--gitlab']:
        repo = emp.clone_from_gitlab(args['--gitlab'])
    elif args['--url']:
        repo = emp.clone_from_url(args['--url'])
    else:
        repo = Path()

    args.update({'<path>': str(Path(args['<path>'])/repo)})


def run_action(args):
    force = args['--force']
    action = args['<action>']
    pattern = '**/' + args['--pattern']

    q = 'Run {0} in {1} ? [y|n] '
    for empfile in Path(args['<path>']).glob(pattern):
        if force or emp.show_prompt(q.format(action, empfile)):
            emp.run(empfile, action, 'utf-8')


def main():
    args = docopt(__doc__, version=emp.__version__)
    set_logging(args)
    clone_repo(args)
    run_action(args)


# main
if __name__ == '__main__':
    main()
