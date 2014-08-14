import sys
import re
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def find_version(fname):
    '''Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    '''
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


def read(fname):
    with open(fname) as fp:
        content = fp.read()
        return content


__version__ = find_version("convoyeur/__init__.py")


setup(
    name='convoyeur',
    version=__version__,
    description='Python programn that upload files',
    long_description=read("README.md"),
    author='Greg Leclercq',
    author_email='greg@botify.com',
    url='https://github.com/botify-labs/convoyeur',
    packages=find_packages(exclude=("test*", )),
    package_dir={'convoyeur': 'convoyeur'},
    include_package_data=True,
    install_requires=[
        'boto',
        'futures', 
    ],
    zip_safe=False,
    keywords='upload',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
    tests_require=['pytest'],
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts': [
            'convoyeur = convoyeur.command:main',
        ]
    }
)
