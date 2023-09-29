import argparse
from pathlib import Path
import subprocess
import json
import yaml
from platform import python_version
import socket
import sys
from thunder.fancylogger import FancyLogger
from itertools import chain


SPECIAL_PACKAGE_MAPPINGS = {
    'thunder': 'thundertools',
    'pil': 'pillow',
    'cv2': 'opencv-python',
    'sklearn': 'scikit-learn',
    'yaml': 'pyyaml'
}


logger = FancyLogger()


def _get_imported_lib(instruction):
    if 'from' in instruction:
        return instruction.replace('from ', '').split(' ')[0]
    return instruction.replace('import ', '').split(' ')[0].rstrip('\n')
    

def _extract_notebook_imports(notebook_name):
    nb_path = (Path('.') / notebook_name).absolute()
    with nb_path.open() as f:
        nb_dict = json.load(f)
    nb_cells_source = [cell['source'] for cell in nb_dict['cells']]
    imports = []
    for cell_source in nb_cells_source:
        cell_imports = [_get_imported_lib(line) for line in cell_source 
                        if line.startswith('import ') or line.startswith('from ')]
        imports.extend(cell_imports)
    return imports


def _extract_py_imports(py_files):
    imports = []
    for py_file in py_files:
        with Path(py_file).open() as f:
            py_lines = f.read().splitlines()
        py_imports = [_get_imported_lib(line) for line in py_lines 
                        if line.startswith('import ') or line.startswith('from ')]
        imports.extend(py_imports)
    return imports


def _extract_pip_packages():
    pip_output = subprocess.check_output(['pip', 'freeze'])
    pip_packages = [line for line in pip_output.decode('utf-8').split('\n') if '==' in line]
    if len(pip_packages) == 0:
        return [], []
    packages, versions = zip(*[line.split('==') for line in pip_packages]) 
    return packages, versions


def _extract_conda_packages():
    conda_output = subprocess.check_output(['conda', 'list'])
    conda_packages = [line for line in conda_output.decode('utf-8').split('\n') 
                      if not line.startswith('#') and len(line) > 1]
    if len(conda_packages) == 0:
        return [], []
    packages, versions, _, sources = zip(*[line.split() for line in conda_packages if len(line.split()) == 4])
    return packages, versions


def is_native_package(package_name):
    if package_name not in sys.modules.keys():
        try:
            __import__(package_name)
        except:
#             print(f'error while scanning: {package_name}, ignoring')
            return True
    return sys.modules[package_name].__package__ == ''


def _get_py_files_recursively(directory):
    py_file_paths = [file.absolute() for file in Path(directory).iterdir() if file.suffix == '.py']
    if not any([file.is_dir() for file in Path(directory).iterdir()]):
        return py_file_paths
    for dir_path in [file for file in Path(directory).iterdir() if file.is_dir()]:
        py_file_paths.extend(_get_py_files_recursively(dir_path))
    return py_file_paths


def _get_packages(imports):
    pip_package_names, pip_package_versions = _extract_pip_packages()
    conda_package_names, conda_package_versions = _extract_conda_packages()
    pip_packages = []
    conda_packages = []
    for package in imports:
        _package = package.lower().replace('_', '-')
        if _package in SPECIAL_PACKAGE_MAPPINGS:
            package = SPECIAL_PACKAGE_MAPPINGS[_package]
            _package = package
        if _package in pip_package_names:
            pip_packages_index = pip_package_names.index(_package)
            pip_packages.append(f'{package}=={pip_package_versions[pip_packages_index]}')
            continue
        if _package in conda_package_names:
            conda_packages_index = conda_package_names.index(_package)
            conda_packages.append(f'{package}=={conda_package_versions[conda_packages_index]}')
            continue
        if '.' in _package:
            base_package_name = package.split('.')[0]
            _base_package_name = _package.split('.')[0]
            if _base_package_name in pip_package_names:
                pip_packages_index = pip_package_names.index(_base_package_name)
                pip_packages.append(f'{base_package_name}=={pip_package_versions[pip_packages_index]}')
                continue
            if _base_package_name in conda_package_names:
                conda_packages_index = conda_package_names.index(_base_package_name)
                conda_packages.append(f'{base_package_name}=={conda_package_versions[conda_packages_index]}')
                continue
#         print(f'could not find a candidate for: {package}')
    return pip_packages, conda_packages
    

def _add_other_pip_urls(env_template):
    if socket.gethostname() == 'brj-ml-server':
        env_template['dependencies'][2]['pip'].append('--extra-index-url http://localhost/simple')
    return env_template


def _add_cuda_libs(env_template):
    cuda_libs = [f'{package}={version}' for package, version in zip(*_extract_conda_packages()) 
                 if package in ['cudatoolkit', 'cudnn']]
    env_template['dependencies'].extend(cuda_libs)
    return env_template


def extract_env_file():
    parser = argparse.ArgumentParser(description='extract the environment from a Jupyter Notebook file and its py files')
    parser.add_argument('-p', '--path', metavar='PATH', help='path to the notebook file')
    args = parser.parse_args()
    assert args.path is not None, 'provide a path to a notebook with flag -p'
    notebook_name = Path(args.path)
    assert Path(notebook_name).is_file(), 'the given path does not exist'
    assert Path(notebook_name).suffix == '.ipynb', 'the given path is not a Jupyter Notebook'
    
    template = {'name': notebook_name.stem, 
                'channels': ['conda-forge'], 
                'dependencies': [
                    f'python={python_version()}', 
                    'pip', 
                    {'pip': []}]}
    template = _add_other_pip_urls(template)
    template = _add_cuda_libs(template)
    nb_imports = _extract_notebook_imports(notebook_name)
    local_package_dirs = [package for package in nb_imports if (Path('.') / package).is_dir()]
    native_packages = [i for i in nb_imports if i not in local_package_dirs and not is_native_package(i)]
    nb_imports = [package for package in nb_imports if package not in local_package_dirs and package not in native_packages]
    py_files = chain(*[_get_py_files_recursively(dir_name) for dir_name in local_package_dirs])
    py_imports = [i for i in _extract_py_imports(py_files) if not is_native_package(i)]
    nb_pip_packages, nb_conda_packages = _get_packages(nb_imports)
    py_pip_packages, py_conda_packages = _get_packages(py_imports)
    template['dependencies'][2]['pip'].extend(set(nb_pip_packages + py_pip_packages))
    template['dependencies'].extend(set(nb_conda_packages + py_conda_packages))
    output_yaml = yaml.dump(template)
    with notebook_name.with_suffix('.yml').open('w') as f:
        f.write(output_yaml)
    print(f'file saved to: {notebook_name.with_suffix(".yml")}')


if __name__ == '__main__':
    extract_env_file()
