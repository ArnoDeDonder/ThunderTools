import os
from pathlib import Path
from time import sleep
from typing import Tuple
from thunder.tools import clear


def _filepicker_in_dir(name: str, start_dir_path: Path, file_type: str, multiple: bool) -> Tuple[Path, bool]:
    clear()
    files_in_dir = ['.', '..'] + [str(file) for file in start_dir_path.iterdir()]
    if file_type == 'DIR':
        files_in_dir = [file for file in files_in_dir if Path(file).is_dir()]  # only look at directories in this flow
    print(f'NAVIGATE TO {name.upper()} '
          f'{"(PRECEDE WITH s TO SELECT THE DIRECTORY)" if file_type == "DIR" else ""}',
          end='\n\n')
    print(f'》{start_dir_path}')
    for i, path in enumerate(files_in_dir, 1):
        print(f'{str(i).ljust(2)}  {"◆" if Path(path).is_dir() else "◇"}  {Path(path).name if path != "." else "." }')
    sleep(0.2)
    choice = input(f'[{1}-{len(files_in_dir)}] : ')
    select_dir = False
    try:
        if choice.startswith('s'):
            select_dir = True
            choice = choice[1:]
        choice = int(choice.strip())
        if choice < 1 or choice > len(files_in_dir):
            raise ValueError('selected option out of bounds')
        return start_dir_path.joinpath(files_in_dir[choice - 1]).resolve(), select_dir
    except ValueError:
        return _filepicker_in_dir(name, start_dir_path, file_type, multiple)


def filepicker(name, start_dir, file_type='FILE', multiple=False):
    assert file_type in ['FILE', 'DIR'], 'not a valid filetypes, pick one of: FILE, DIR'
    current_dir = Path(start_dir).absolute()
    current_dir.mkdir(parents=True, exist_ok=True)
    out_value = '' if not multiple else []
    while True:
        chosen_file, select_dir = _filepicker_in_dir(name=name,
                                                     start_dir_path=current_dir,
                                                     file_type=file_type,
                                                     multiple=multiple)
        if (file_type == 'FILE' and chosen_file.is_dir()) or (file_type == 'DIR' and not select_dir):
            current_dir = chosen_file
            continue
        if multiple:
            out_value.append(chosen_file)
            clear()
            print('SELECTED PATHS:')
            print('\n'.join([f'→ {path.name}' for path in set(out_value)]), end='\n\n')
            if input('SELECT ANOTHER PATH? (y/N) : ').lower() == 'y':
                continue
        else:
            out_value = chosen_file
        break
    return out_value
