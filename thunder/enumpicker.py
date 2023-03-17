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


def enumpicker(name, possible_values, default_value):
    assert default_value in possible_values, 'provide a default value from the list of possible values'
    out_value = None
    while out_value == None:
        clear()
        print(f'Select: {name.upper()}')
        sleep(0.2)
        for i, value in enumerate(possible_values, 1):
            print(
                f'{str(i).ljust(2)}  {"◆" if value == default_value else "◇"}  {value}')
        sleep(0.2)
        try:
            choice = input(f'[{1}-{len(possible_values)}] : ')
            if choice == '':
                out_value = default_value
                continue
            choice = int(choice)
            assert choice >= 1
            assert choice <= len(possible_values)
            out_value = possible_values[choice - 1]
        except (ValueError, AssertionError):
            continue
    clear()
    return out_value
