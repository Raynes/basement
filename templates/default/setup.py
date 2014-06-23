"""Your project's description"""
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='{{project-name}}',
    description="A project that does things!",
    version='0.1.0',
    long_description=__doc__,
    packages=['{{project-name}}'],
    author='John Doe',
    author_email='you@yoursite.com',
    url='https://github.com/you/{{project-name}}',
    license='MIT',
    install_requires=requirements
)
