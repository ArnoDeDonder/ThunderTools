import os
import getpass
import socket
import builtins
from enum import Enum
from datetime import datetime

from colorama import init as colorama_init


colorama_init()


class EnvType(Enum):
    JUPYTER = 'Jupyter'
    IPYTHON = 'IPython'
    SHELL = 'Shell'


def get_env_type():
    if hasattr(builtins, '__JUPYTER__'):
        return EnvType.JUPYTER
    elif hasattr(builtins, '__IPYTHON__'):
        return EnvType.IPYTHON
    else:
        return EnvType.SHELL


def _clear_terminal():
    clear_screen = "\033[2J"
    move_to_top = "\033[H"
    clear_screen_and_move_top = clear_screen + move_to_top
    os.system(f'echo {clear_screen_and_move_top}')


ENVIRONMENT = get_env_type()
if ENVIRONMENT != EnvType.SHELL:
    from IPython.display import clear_output
    clear = clear_output
else:
    clear = _clear_terminal


def get_system_user():
    return getpass.getuser()


def get_system_name():
    return socket.gethostname()


def get_current_formatted_datetime():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
