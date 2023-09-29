import os
import re
from functools import reduce
from pathlib import Path

from thunder import boolpicker, stringpicker
from thunder.tools import clear


def _correct_name(name: str):
    return re.sub(r"\s", "_", name.upper())


class CredentialsNotCreatedException(BaseException):
    pass


class ThunderCredentials:
    def __init__(self, creds_name: str, to_env=False):
        self.creds_name = creds_name
        creds_path = Path.home() / f'.{_correct_name(creds_name).lower()}'
        if not creds_path.is_file():
            make_creds_file = boolpicker(f'credentials [{creds_name}] do not exist, do you want to build them?')
            clear()
            if not make_creds_file:
                raise CredentialsNotCreatedException
            variable_name = stringpicker('key name', '')
            variable_value = stringpicker('value', '')
            variables = {variable_name: variable_value}
            clear()
            while boolpicker('add another variable?'):
                variable_name = stringpicker('key name', '')
                variable_value = stringpicker('value', '')
                variables[variable_name] = variable_value
                clear()
            longest_variable_name = max([len(v) for v in variables])
            print(f'Following variables will be written to {str(creds_path)}:')
            for variable_name in variables:
                print(f'    {_correct_name(variable_name).ljust(longest_variable_name)} = {variables[variable_name]}')
            creds_path.write_text(reduce(
                lambda c, v: c + f'{_correct_name(v[0])} = {v[1]}\n',
                variables.items(),
                ''
            ).strip())
        for line in creds_path.read_text().splitlines():
            if len(line.strip()) == 0:
                continue
            variable_name, variable_value = line.split(' = ')
            if to_env:
                os.environ[variable_name] = variable_value
            setattr(self, variable_name, variable_value)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        output = f'ThunderCredentials (.{self.creds_name})'
        longest_var = max([len(v) for v in vars(self) if v != 'creds_name'])
        for var in vars(self):
            if var == 'creds_name':
                continue
            output += f'\n    {_correct_name(var).ljust(longest_var)} = {vars(self)[var]}'
        return output
