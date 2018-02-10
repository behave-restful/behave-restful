"""
Setup for behave-restful
"""
from setuptools import setup, find_packages
import behave_restful.about as about

packages = find_packages()
requirements = [
    "behave>=1.2.5",
    "jsonpath-rw>=1.4.0",
    "jsonschema>=2.6.0",
    "requests>=2.18.4"
]


setup(
    name=about.project,
    version=about.release,
    author=about.author,
    author_email=about.author_email,
    packages=packages,
    install_requires=requirements
)
