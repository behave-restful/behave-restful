"""
Setup for behave-restful
"""
from setuptools import setup, find_packages
import behave_restful.about as about

def _read_dependencies():
    requirements_file = 'dependencies.txt'
    with open(requirements_file) as fin:
        return [line.strip() for line in fin if line]


packages = find_packages()
requirements = _read_dependencies()


setup(
    name=about.project,
    version=about.release,
    author=about.author,
    author_email=about.author_email,
    packages=packages,
    install_requires=requirements
)
