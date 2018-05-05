# coding: utf-8

from __future__ import absolute_import, print_function, unicode_literals

# public items
__all__ = ['call',
           'clone_from_github',
           'clone_from_gitlab',
           'clone_from_url',
           'show_prompt']

# standard library
import re
import sys
from logging import getLogger
from subprocess import Popen, PIPE, STDOUT

# dependent packages
from pathlib2 import Path

# module logger
logger = getLogger(__name__)

# module constants
CMD_GITHUB = 'git clone https://github.com/{0}'
CMD_GITLAB = 'git clone https://gitlab.com/{0}'
CMD_URL    = 'git clone {0}'

# Python 2/3 matters
if sys.version_info.major == 2:
    input = raw_input


# functions
def call(cmd, cwd=None, encoding='utf-8'):
    """Run shell script and log stdout.

    Args:
        cmd (str):
        cwd (str or path):
        encoding (str):

    Returns:
        returncode (int):

    """
    if not isinstance(cmd, str):
        logger.warning('warn')
        return 127

    if cwd is not None:
        cwd = str(Path(cwd).expanduser())

    proc = Popen(cmd, cwd=cwd, shell=True,
                 stdout=PIPE, stderr=STDOUT)

    def getlines():
        while True:
            line = proc.stdout.readline()
            if line:
                yield line.decode(encoding)
            else:
                if proc.poll() is not None:
                    break

    for line in getlines():
        logger.info(line.rstrip('\n'))

    return proc.returncode


def clone_from_github(user_repo, cwd=None, encoding='utf-8'):
    call(CMD_GITHUB.format(user_repo), cwd, encoding)
    return Path(user_repo.rstrip('.git').split('/')[-1])


def clone_from_gitlab(user_repo, cwd=None, encoding='utf-8'):
    call(CMD_GITLAB.format(user_repo), cwd, encoding)
    return Path(user_repo.rstrip('.git').split('/')[-1])


def clone_from_url(url, cwd=None, encoding='utf-8'):
    call(CMD_URL.format(url), cwd, encoding)
    return Path(url.rstrip('.git').split('/')[-1])


def show_prompt(question, pattern_true='^[Y|y]'):
    answer = input(question)
    logger.info('{0} --> {1}'.format(question, answer))
    return bool(re.search(pattern_true, answer))
