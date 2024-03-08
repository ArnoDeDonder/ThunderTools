import os
import zipfile
from typing import Union
from pathlib import Path


def zipit(input_path: Union[Path, str], output_path: Union[Path, str]):
    input_path = Path(input_path)
    output_path = Path(output_path)
    if not input_path.exists():
        raise FileNotFoundError(f"the given input path {input_path} does not exist")
    if output_path.is_dir() or not output_path.suffix:
        output_path = output_path / (input_path.name + '.zip')
    else:
        if not output_path.suffix == '.zip':
            output_path = output_path.with_suffix('.zip')
    output_dir = output_path.parent
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    # calculate original size
    original_size = 0
    if input_path.is_file():
        original_size = input_path.stat().st_size
    elif input_path.is_dir():
        for dir_path, dir_names, file_names in os.walk(input_path):
            for file_name in file_names:
                file_path = os.path.join(dir_path, file_name)
                original_size += os.path.getsize(file_path)

    # build zip file
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        if input_path.is_file():
            zipf.write(input_path, arcname=input_path.name)
        elif input_path.is_dir():
            for root, _, files in os.walk(input_path):
                for file in files:
                    file_path = Path(root) / file
                    zipf.write(file_path, arcname=file_path.relative_to(input_path))

    zipped_size = output_path.stat().st_size
    print(f'original size of {input_path.name}: {(original_size / 1024 / 1024):.3f} Mb')
    print(f'zipped size of {output_path.name}: {(zipped_size / 1024 / 1024):.3f} Mb')
