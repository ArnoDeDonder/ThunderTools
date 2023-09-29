import os
from time import sleep
from thunder.tools import clear


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
