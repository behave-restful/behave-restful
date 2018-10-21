"""
Setup for behave-restful
"""
from setuptools import setup, find_packages
from os import path

from m2r import parse_from_file

import behave_restful.about as about

readme_file = path.join(path.dirname(path.abspath(__file__)), 'README.md')
readme = parse_from_file(readme_file)

def _read_dependencies():
    requirements_file = 'dependencies.txt'
    with open(requirements_file) as fin:
        return [line.strip() for line in fin if line]

packages = find_packages()
requirements = _read_dependencies()


setup(
    name=about.project,
    version=about.release,
    description=about.description,
    long_description=readme,
    author=about.author,
    author_email=about.author_email,
    url=about.url,
    license=about.license,
    keywords=about.keywords,
    classifiers=about.classifiers,
    packages=packages,
    install_requires=requirements
)
