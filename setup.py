from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='behave-restful',  # Required

    version='0.0.1',  # Required

    description='BDD Framework for testing REST services and APIs',  # Required

    long_description=long_description,  # Optional

    url='https://github.com/behave-restful/behave-restful',  # Optional

    author='Isaac Rodriguez',  # Optional

    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='BDD testing development RESTful automation',  # Optional
    
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    install_requires=['behave', 'bolt-ta', 'conttest', 'coverage', 'nose', 'assertpy'],  # Optional

    extras_require={  # Optional
        'dev': ['pylint', 'sphinx'],
        'test': [
        ],
    },
)