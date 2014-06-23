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
    author='{{full-name}}',
    author_email='{{email}}',
    url='https://github.com/{{github-user}}/{{project-name}}',
    license='{{license}}',
    install_requires=requirements
)
