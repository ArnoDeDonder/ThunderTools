from time import sleep
from thunder.tools import clear


def boolpicker(name, default=True) -> bool:
    question = name.rstrip('?').upper() + '?'
    while True:
        clear()
        print(question)
        sleep(0.2)
        print(f'T  {"◆" if default == True else "◇"}  True')
        print(f'F  {"◆" if default == False else "◇"}  False')
        sleep(0.2)
        try:
            choice = input(f'[T-F] : ')
            if choice == '':
                clear()
                return default
            if choice.lower() == 't':
                clear()
                return True
            if choice.lower() == 'f':
                clear()
                return False
        except ValueError:
            pass
