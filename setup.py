from setuptools import setup, find_packages

setup(
    name='thundertools',
    version='0.2.2',
    author='Arno De Donder',
    author_email='arno.dedonder@hotmail.com',
    description='Different tools for working with jupuyter notebooks',
    packages=find_packages(),
    install_requires=[
        'IPython',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
    entry_points={
        'console_scripts': [
            'export_conda=thunder.export_conda:extract_env_file'
        ]
    }
)
