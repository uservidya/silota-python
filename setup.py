import os, re
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

def _get_version():
    path = os.path.join(here, 'silota', '__init__.py')
    version_re = r".*__version__ = '(.*?)'"
    fo = open(path, 'r')
    try:
        return re.compile(version_re, re.S).match(fo.read()).group(1)
    finally:
        fo.close()


def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements

VERSION = _get_version()

README = open(os.path.join(here, "README.rst")).read()
#README = README + open(os.path.join(here, "CHANGES.txt")).read()

setup(
    name='silota',
    version=VERSION,
    author='Ganesh Swami',
    author_email='support@silota.com',
    url='http://www.silota.com',
    packages=['silota'],
    license='BSD',
    description='Python client for the Silota Search As A Service API',
    long_description=README,
    test_suite = 'nose.collector',
    install_requires=parse_requirements('requirements.txt'),    
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

)
