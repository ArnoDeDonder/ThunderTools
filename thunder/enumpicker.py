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


def _get_value_indicator(default_value, multiple, out_value, current_value):
    if current_value in out_value:
        return '✚'
    if (not multiple or len(out_value) == 0) and default_value == current_value:
        return '◆'
    return '◇'


def enumpicker(name, possible_values, default_value, multiple=False):
    assert default_value in possible_values, 'provide a default value from the list of possible values'
    out_value = '' if not multiple else []
    finished = False
    while not finished:
        clear()
        print(f'Select: {name.upper()}')
        sleep(0.2)
        for i, value in enumerate(possible_values, 1):
            print(
                f'{str(i).ljust(2)}  {_get_value_indicator(default_value, multiple, out_value, value)}  {value}')
        sleep(0.2)
        try:
            choice = input(f'[{1}-{len(possible_values)}] : ')
            if choice == '':
                if multiple:
                    if len(out_value) == 0:
                        out_value.append(default_value)
                    finished = True
                    continue
                out_value = default_value
                finished = True
                continue
            choice = int(choice)
            assert choice >= 1
            assert choice <= len(possible_values)
            selected_value = possible_values[choice - 1]
            if multiple:
                out_value.append(selected_value)
                continue
            out_value = selected_value
            finished = True
        except (ValueError, AssertionError):
            continue
    clear()
    if isinstance(out_value, list):
        out_value = list(set(out_value))
    return out_value
