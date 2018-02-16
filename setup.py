from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import re
import sys

"""
DEVELOPMENT SETUP

This will get the necessary environment setup to use the source of ZeexApp.
This will be complied into an executeable though and distributed so normal users
probably wouldn't want to install this way unless.
"""

here = os.path.abspath(os.path.dirname(__file__))

__version__ = '1.0'


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


short_description = """NHTSA vehicle API for decoding VIN and more."""

try:
    long_description = read('README.md')
except:
    long_description = "See README.md where installed"


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


tests_require = ['requests']
setup(
    name='pynhtsa',
    version=__version__,
    url='https://github.com/zbarge/pynhtsa',
    license='MIT',
    namespace_packages=['pynhtsa'],
    author='Zeke Barge',
    tests_require=tests_require,
    install_requires=['requests'],

    cmdclass={'test': PyTest},
    author_email='zekebarge@gmail.com',
    description=short_description,
    long_description=long_description,
    include_package_data=True,
    packages=['pynhtsa'],

    platforms='any',
    test_suite='tests',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces'
    ],
    extras_require={
        'testing': tests_require,
    },
)
