# Thundertools

This repository contains some handy tools for working in python. 
The tools are mainly designed to be used in a shell but are also functional in Jupyter.

### Installation

```shell
pip install thundertools
```

## Features

### Small tools

#### Check what python environment you are in
```python
from thunder import ENVIRONMENT
print(ENVIRONMENT.value)
```

#### Clear your output
```python
from thunder.tools import clear
clear()
```

#### Get the name of the system and user
```python
from thunder.tools import get_system_name, get_system_user
print(get_system_name())
print(get_system_user())
```

#### Get current datetime as a nice string
```python
from thunder.tools import get_current_formatted_datetime
print(get_current_formatted_datetime())
```

### Stylish logging with datetime and log level
```python
from thunder import FancyLogger

logger = FancyLogger()

logger.set_log_level('debug')

logger.log('this will be in debug since this is the log level')
logger.debug('we are making a call to somewhere')
logger.info('data extracted')
logger.warn('watch out, this data is not as expected')  # or logger.warning
logger.error('something has gone wrong!')
logger.crit('critical state, exiting')  # or logger.critical
```

### User input

##### boolpicker
```python
from thunder import boolpicker

use_gpu = boolpicker('use a gpu?', False)
print(f'use gpu: {use_gpu}')
```

##### stringpicker
```python
from thunder import stringpicker

project_name = stringpicker('a project name', 'test_project')
print(f'project_name: {project_name}')
```

##### numberpicker
```python
from thunder import numberpicker

epochs = numberpicker('amount of epochs', 5)
print(f'amount of epochs: {epochs}')
```

##### enumpicker

```python
from thunder import enumpicker

log_level = enumpicker('log level', ['DEBUG', 'INFO', 'WARNING', 'ERROR'], 'INFO')
print(f'log level: {log_level}')
```

##### filepicker
```python
from thunder import filepicker

model_path = filepicker('the model path', 
                        '/mnt/hdd/shared/employee/klassifai', 
                        'FILE', 
                        multiple=False)

print(f'model path: {model_path}')
```

### ThunderCredentials
```python
from thunder import ThunderCredentials
credentials = ThunderCredentials('name')
```