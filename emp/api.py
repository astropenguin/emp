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
from functools import partial
from logging import getLogger
logger = getLogger(__name__)

# dependent packages
import emp
from pathlib2 import Path

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
        finished with no problem (bool):

    """
    path = Path(empfile).expanduser()

    if not path.exists():
        logger.warning('warn')
        return False

    if action == REQUIREMENTS:
        logger.warning('warn')
        return False

    if not meet_requirements(empfile, encoding):
        logger.warning('warn')
        return False

    with path.open('r') as f:
        try:
            cmd = yaml.load(f)[action]
        except KeyError:
            logger.warning('warn')
            return True
        except:
            logger.warning('warn')
            return False

    emp.call(cmd, path.parent, encoding)
    return True


def meet_requirements(empfile, encoding='utf-8'):
    path = Path(empfile).expanduser()

    if not path.exists():
        logger.warning('warn')
        return False

    with path.open('r') as f:
        try:
            reqs = yaml.load(f)[REQUIREMENTS]
        except KeyError:
            logger.warning('warn')
            return True
        except:
            logger.warning('warn')
            return False

    def meet(name, cmds):
        if not emp.call(cmds['try'], path.parent, encoding):
            logger.info('info')
            return True

        emp.call(cmds['except'], path.parent, encoding)

        if not emp.call(val['try'], path.parent, encoding):
            logger.info('info')
            return True
        else:
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
