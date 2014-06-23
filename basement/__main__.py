"""Entry point"""
import sys
import click
from os.path import abspath

from basement.process import process, AlreadyExistsError
from basement.config import TemplateDoesntExistError


@click.command()
@click.argument('directory')
@click.option('--template', '-t', default='default',
              help="The name of the template to use.")
@click.option('--verbose', '-v', is_flag=True,
              help="When verbose is true, the template data is printed.")
def ment(directory, template, verbose):
    """Generate a Python project based on a template.
    Templates are stored in ~/.basement-templates and
    are simply mustache templates that are rendered
    against the configuration you've specified in the
    toml-formatted ~/.basement config file. Any top
    level keys are merged in with keys from sections
    named after specific templates.

    """
    try:
        process(template, directory, verbose=verbose)
    except AlreadyExistsError as e:
        print(e)
        sys.exit(1)
    except TemplateDoesntExistError as e:
        print("That template doesn't exist!")
        sys.exit(1)
