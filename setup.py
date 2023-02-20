from setuptools import setup, find_packages

setup(
    name='thundertools',
    version='0.0.1',
    author='Arno De Donder',
    author_email='arno.dedonder@hotmail.com',
    description='Different tools for working with jupuyter notebooks',
    packages=find_packages(),
    install_requires=[
        'IPython',
        'ipyparams'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)