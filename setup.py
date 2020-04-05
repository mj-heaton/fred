from collections import namedtuple

import setuptools
from fred import __version__

ToolChain = namedtuple('ToolChain', ('c', 'cxx'))


setuptools.setup(
    name='fred',
    version=__version__,
    description='A toolbox for building financial forecasts for SMEs',
    url='https://fred.io',
    author='Matthew Heaton',
    license='MIT',
    zip_safe=True,
    python_requires='>=3.6.0',
    install_requires=[
    ],
    package_dir={'fred': 'fred'},
    packages=setuptools.find_packages(
        exclude=['benchmarks', 'benchmarks.*', 'tests', 'tests.*']
    ),
    include_package_data=True,  # (MANIFEST.in)
    command_options={
        'build_sphinx': {
            'source_dir': ('setup.py', 'docs/source'),
            'warning_is_error': ('setup.py', True)
        }
    },
)
