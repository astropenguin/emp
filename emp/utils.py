# coding: utf-8

from __future__ import absolute_import, print_function, unicode_literals

# public items
__all__ = ['call',
           'from_github',
           'from_gitlab',
           'from_url']

# standard library
from pathlib2 import Path
from logging import getLogger
from subprocess import Popen, PIPE, STDOUT
logger = getLogger(__name__)

# module constants
URL_GITHUB = 'https://github.com/{0}/{1}.git'
URL_GITLAB = 'https://gitlab.com/{0}/{1}.git'


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


def from_github(user, repo, cwd=None, encoding='utf-8'):
    cmd = 'git clone ' + URL_GITHUB.format(user, repo)
    call(cmd, cwd, encoding)


def from_gitlab(user, repo, cwd=None, encoding='utf-8'):
    cmd = 'git clone ' + URL_GITLAB.format(user, repo)
    call(cmd, cwd, encoding)


def from_url(url, cwd=None, encoding='utf-8'):
    cmd = 'git clone ' + url
    call(cmd, cwd, encoding)
