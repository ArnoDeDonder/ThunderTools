import os
from time import sleep
from thunder.tools import clear

    
def numberpicker(name, default_value):
    assert str(default_value).isnumeric(), 'provide a number as default value'
    default_value = int(default_value)
    out_value = None
    while out_value is None:
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
