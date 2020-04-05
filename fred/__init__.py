""" This is the main fred package,
    all fred code lives within this """
import subprocess
from pkgutil import get_data
import platform
import os
import socket

from fred.core.config import FredConfig

FRED_MAJOR_VERSION = 0
FRED_MINOR_VERSION = 0
FRED_PATCH_VERSION = 0
FRED_DEV_VERSION = ''

__version__ = (f'{FRED_MAJOR_VERSION}.{FRED_MINOR_VERSION}'
               f'.{FRED_PATCH_VERSION}{FRED_DEV_VERSION}')

FRED_CONFIG = FredConfig()


def get_plot(grid=True):
    import matplotlib.pyplot as plt
    plt.clf()
    plt.close()

    plt.rcParams["figure.figsize"] = (20, 10)

    if grid:
        plt.minorticks_on()
        plt.grid(b=True, which='major', color='k', linestyle='-')
        plt.grid(b=True, which='minor', color='k', linestyle='--', alpha=0.2)

    return plt


def try_get_git_hash() -> str:

    sha = os.getenv('FRED_GIT_SHA')
    branch = os.getenv('FRED_GIT_BRANCH')

    if sha or branch:
        if str(branch).strip() == '':
            branch = 'DETACHED'

        return str(sha) + ':' + str(branch)

    try:
        git_hash = subprocess.check_output(
            ['git', 'describe', '--always', '--dirty']).strip().decode("utf-8")
        git_branch = subprocess.check_output(
            ['git', 'rev-parse',
             '--abbrev-ref', 'HEAD']).strip().decode("utf-8")

        return git_hash + ":" + git_branch

    except Exception:
        pass

    try:
        return get_data('fred',
                        'git-describe.txt').decode("utf-8").replace('\n', '')
    except Exception:
        pass

    try:
        with open('/fred/fred/git-describe.txt', 'r') as desc:
            return desc.read().replace('\n', '')
    except Exception:
        pass

    try:
        with open('/git-describe.txt', 'r') as desc:
            return desc.read().replace('\n', '')
    except Exception:
        pass

    return 'unknown'


def get_nice_version_str():
    return try_get_git_hash() + ":" + __version__


__fred_dict__ = {
    'revision': try_get_git_hash(),
    'majorVersion': FRED_MAJOR_VERSION,
    'minorVersion': FRED_MINOR_VERSION,
    'patchVersion': FRED_PATCH_VERSION,
    'devVersion': FRED_DEV_VERSION,
    'version': __version__
}

__fred_python__ = {
    'version': platform.python_version(),
    'compiledWith': platform.python_compiler()
}

try:
    __fred_docker_version__ = os.environ['DOCKER_IMAGE_ID']
except KeyError:
    __fred_docker_version__ = "null"

try:
    __fred_hostname__ = os.environ['FRED_HOSTNAME']
except KeyError:
    __fred_hostname__ = socket.gethostname()
