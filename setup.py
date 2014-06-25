"""A tool for generating Python project scaffolding based on
user defined templates.

"""
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('README.md') as f:
    description = f.read()

setup(
    name='basement',
    description="A python project scaffolding generator.",
    version='0.1.5',
    long_description=description,
    packages=['basement'],
    include_package_data=True,
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
