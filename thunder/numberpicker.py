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
    
def numberpicker(name, default_value):
    assert str(default_value).isnumeric(), 'provide a number as default value'
    out_value = None
    while out_value == None:
        clear()
        print(f'Select: {name.upper()}')
        sleep(0.2)
        choice = input(f'Default [{default_value}] : ')
        if choice == '':
            out_value = default_value
            continue
        if choice.isnumeric():
            if int(choice) == float(choice):
                out_value = int(choice)
                continue
            out_value = float(choice)
            continue
    clear()
    return out_value