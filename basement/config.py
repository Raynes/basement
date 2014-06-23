"""Configuration for basement and templates."""
import sys
import os
from os import path
from shutil import copytree
from pkg_resources import resource_filename, Requirement

import toml

# WHAT DOES IT ALL MEAAAAAAAAN
THIS = Requirement.parse('basement')

TEMPLATES_DIR = path.expanduser('~/.basement-templates')

# Create the templates directory if it doesn't exist.
if not path.isdir(TEMPLATES_DIR):
    copytree(resource_filename(THIS, 'templates'), TEMPLATES_DIR)
else:
    pass # TODO: Update things


try:
    with open(path.expanduser('~/.basement'), 'r') as config:
        CONFIG = toml.loads(config.read())
except IOError as e:
    if e.errno == 2:
        print("Config file doesn't exist!")
    else:
        print("Something went wrong :(!")
    sys.exit(1)


def base_config():
    """Get the base configuration without sections"""
    return {k: v
            for k, v
            in CONFIG.iteritems()
            if not isinstance(v, dict)}


class TemplateDoesntExistError(Exception):
    pass


def lookup_template(name):
    """Returns the path to a template or throws
    an exception if the template wasn't found.

    """
    template_path = path.join(TEMPLATES_DIR, name)
    if path.isdir(template_path):
        return template_path
    else:
        raise TemplateDoesntExistError()


def template_config(name):
    """Read the configuration for a specific template."""
    base = base_config()
    template = CONFIG.get(name, {})
    # Merging intensifies
    base.update(template)
    return base
