import os
from time import sleep
from thunder.tools import get_shell_type

SHELL_TYPE = get_shell_type()


def _clear_terminal():
    with open(os.devnull, 'w') as devnull:
        print(os.system('clear'), file=devnull)


if SHELL_TYPE != 'TERMINAL':
    from IPython.display import clear_output

    clear = clear_output
else:
    clear = _clear_terminal


def stringpicker(name, default_value):
    assert isinstance(default_value, str), 'provide a string as default value'
    clear()
    print(f'Write: {name.upper()}')
    sleep(0.2)
    choice = input(f'[{default_value}] : ')
    if choice == '':
        return default_value
    clear()
    return choice
