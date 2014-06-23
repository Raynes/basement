"""A tool for generating Python project scaffolding based on
user defined templates.

"""
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='basement',
    description="A python project scaffolding generator.",
    version='0.1.0',
    long_description=__doc__,
    packages=['basement'],
    author='Anthony Grimes',
    author_email='i@raynes.me',
    url='https://github.com/Raynes/basement',
    license='MIT',
    install_requires=requirements,
    entry_points = """
    [console_scripts]
    basement=basement.__main__:ment
    ment=basement.__main__:ment
    """
)
