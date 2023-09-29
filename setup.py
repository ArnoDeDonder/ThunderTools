from setuptools import setup, find_packages

from thunder import __version__


with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='thundertools',
    version=__version__,
    author='Arno De Donder',
    author_email='arno.dedonder@hotmail.com',
    description='Different tools for working in Python',
    licence='MIT',
    url='https://github.com/ArnoDeDonder/ThunderTools',
    keywords=['python', 'tools', 'utility', 'shell', 'terminal', 'scripts', 'linux'],
    packages=find_packages(),
    install_requires=requirements,
    tests_require=[
        'pytest',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    # entry_points={
    #     'console_scripts': [
    #         'export_conda=thunder.export_conda:extract_env_file'
    #     ]
    # }
)
