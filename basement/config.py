"""Configuration for basement and templates."""
import sys
import os
from os import path
from shutil import copytree, rmtree
from pkg_resources import resource_filename

import toml


BUILT_IN_DIR = resource_filename('basement', 'templates')
TEMPLATES_DIR = path.expanduser('~/.basement-templates')


def rename_templates(template_path):
    """Rename all *.basement-template files"""
    for dirpath, _, files in os.walk(template_path):
        for f in files:
            name, ext = path.splitext(f)
            if ext == '.basement-template':
                os.rename(path.join(dirpath, f),
                          path.join(dirpath, name))


# Create the templates directory if it doesn't exist.
if not path.isdir(TEMPLATES_DIR):
    copytree(BUILT_IN_DIR, TEMPLATES_DIR)
    for template_path in os.listdir(TEMPLATES_DIR):
        rename_templates(path.join(TEMPLATES_DIR, template_path))
else:
    old = set(os.listdir(TEMPLATES_DIR))
    new = os.listdir(BUILT_IN_DIR)
    # Every run will delete and replace built in templates
    # This isn't optimal, since it takes time, but it is
    # a very small amount of time and work and makes sure
    # everyone's basement-shipped templates are consistent
    # over versions. They're not meant to be modified.
    for template in new:
        old_path = path.join(TEMPLATES_DIR, template)
        new_path = path.join(BUILT_IN_DIR, template)
        if template in old:
            rmtree(old_path)
        else:
            print("Adding new template {}...".format(template))
        copytree(new_path, old_path)
        rename_templates(old_path)


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
