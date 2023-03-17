import os
from pathlib import Path
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


def _filepicker_in_dir(name, dir_path, multiple, out_length):
    clear()
    files_in_dir = ['.', '..'] + list(dir_path.iterdir())
    print(f'NAVIGATE TO {name.upper()} {f"({out_length})" if multiple else ""}', end='\n\n')
    print(f'》{dir_path}')
    for i, path in enumerate(files_in_dir, 1):
        print(f'{str(i).ljust(2)}  {"◆" if Path(path).is_dir() else "◇"}  {Path(path).name if path != "." else "." }')
    sleep(0.2)
    choice = input(f'[{1}-{len(files_in_dir)}] : ')
    try:
        if choice == '':
            return '.'
        if multiple and choice == 'q':
            return 'q'
        choice = int(choice)
        assert choice >= 1
        assert choice <= len(files_in_dir)
        return files_in_dir[choice - 1]
    except (ValueError, AssertionError):
        return _filepicker_in_dir(name, dir_path)


def filepicker(name, start_dir, file_type='FILE', multiple=False):
    assert file_type in ['FILE', 'DIR'], 'valid filetypes: FILE, DIR'
    current_dir = Path(start_dir).absolute()
    out_value = None if not multiple else []
    while True:
        chosen_file = _filepicker_in_dir(name, current_dir, multiple, len(out_value))
        if multiple and chosen_file == 'q':
            break
        if file_type == 'FILE':
            if (current_dir / chosen_file).is_file():
                if not multiple:
                    out_value = current_dir / chosen_file
                    break
                out_value.append(current_dir / chosen_file)
                continue
            if chosen_file == '.':
                continue
            if chosen_file == '..':
                current_dir = current_dir.parent
                continue
            current_dir = current_dir / chosen_file
            continue
        if chosen_file == '.':
            if not multiple:
                out_value = current_dir
                break
            out_value.append(current_dir)
            continue
        if chosen_file == '..':
            current_dir = current_dir.parent
            continue
        current_dir = current_dir / chosen_file
    clear()
    return out_value