import os
from pathlib import Path
from thunder import FancyLogger
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


def _filepicker_in_dir(dir_path):
    clear()
    files_in_dir = ['.', '..'] + list(dir_path.iterdir())
    print(f'NAVIGATE')
    for i, path in enumerate(files_in_dir, 1):
        print(f'{str(i).ljust(2)}  {"◆" if Path(path).is_dir() else "◇"}  {Path(path).name if path != "." else "." }')
    sleep(0.1)
    choice = input(f'[{1}-{len(files_in_dir)}] : ')
    try: 
        choice = int(choice)
        assert choice >= 1
        assert choice <= len(files_in_dir)
        return files_in_dir[choice - 1]
    except (ValueError, AssertionError):
        return _filepicker_in_dir(dir_path)
    


def filepicker(start_dir, file_type='FILE'):
    assert file_type in ['FILE', 'DIR'], 'valid filetypes: FILE, DIR'
    current_dir = Path(start_dir).absolute()
    target_found = False
    while not target_found:
        chosen_file = _filepicker_in_dir(current_dir)
        print(chosen_file)
        if file_type == 'FILE':
            if (current_dir / chosen_file).is_file():
                clear()
                return current_dir / chosen_file
            if chosen_file == '..':
                current_dir = current_dir.parent
                continue
            current_dir = current_dir / chosen_file
            continue
        if chosen_file == '.':
            clear()
            return current_dir
        if chosen_file == '..':
            current_dir = current_dir.parent
            continue
        current_dir = current_dir / chosen_file