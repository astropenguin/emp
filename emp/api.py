# coding: utf-8

from __future__ import absolute_import, print_function, unicode_literals

# public items
__all__ = ['run',
           'meet_requirements',
           'backup',
           'restore',
           'install',
           'uninstall']

# standard library
from logging import getLogger, INFO, DEBUG
from functools import partial

# dependent packages
import emp
import yaml
from pathlib2 import Path

# module logger
logger = getLogger(__name__)

# module constants
REQUIREMENTS = 'requirements'


# functions
def run(empfile, action, encoding='utf-8'):
    """Read empfile and run action of it.

    Args:
        empfile (str or path):
        action (str):
        encoding (str):

    Returns:
        returncode (int):

    """
    path = Path(empfile).expanduser()
    cwd = path.parent

    if not path.exists():
        logger.warning('warn')
        return None

    if action == REQUIREMENTS:
        logger.warning('warn')
        return None

    with path.open('r', encoding=encoding) as f:
        try:
            cmd = yaml.load(f)[action]
        except KeyError:
            logger.warning('warn')
            return None
        except:
            logger.warning('warn')
            return None

    if not meet_requirements(empfile, encoding):
        logger.warning('warn')
        return None
    else:
        return emp.call(cmd, cwd, INFO, encoding)


def meet_requirements(empfile, encoding='utf-8'):
    """Read empfile and check all requirements are met.

    Args:
        empfile (str or path):
        encoding (str):

    Returns
        all requirements are met (bool):

    """
    path = Path(empfile).expanduser()
    cwd = path.parent

    def meet(name, cmds):
        if not emp.call(cmds['try'], cwd, DEBUG, encoding):
            logger.info('info')
            return True

        emp.call(cmds['except'], cwd, DEBUG, encoding)

        if not emp.call(cmds['try'], cwd, DEBUG, encoding):
            logger.info('info')
            return True
        else:
            logger.warning('warn')
            return False

    if not path.exists():
        logger.warning('warn')
        return False

    with path.open('r', encoding=encoding) as f:
        try:
            reqs = yaml.load(f)[REQUIREMENTS]
        except KeyError:
            logger.warning('warn')
            return True
        except:
            logger.warning('warn')
            return False

    if all(meet(name, cmds) for name, cmds in reqs.items()):
        logger.info('info')
        return True
    else:
        logger.warning('info')
        return False


# aliases
backup = partial(run, action='backup')
restore = partial(run, action='restore')
install = partial(run, action='install')
uninstall = partial(run, action='uninstall')
