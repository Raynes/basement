import os
from os import path
from shutil import copytree
from pprint import pprint

from pystache import render

from basement import config


class AlreadyExistsError(Exception):
    pass


def apply_to_name(data, name):
    """Rename a file assumed to have a mustache template
    in its name to the name with the template rendered.

    """
    os.rename(name, render(name, data))


def apply_to_contents(data, name):
    """Render a template file, replacing it in place.

    """
    with open(name, 'r+') as f:
        contents = f.read()
        f.seek(0)
        f.write(render(contents, data))
        f.truncate()


def process(template, output, verbose=False):
    """Process a template directory, creating our final output"""
    if path.exists(output):
        raise AlreadyExistsError("Output path already exists!")
    else:
        data = config.template_config(template)
        data['project-name'] = path.basename(output)
        if verbose:
            print("Data is:")
            pprint(data)
        copytree(config.lookup_template(template), output)
        for dirpath, directories, files in os.walk(output):
            for f in files + directories:
                f = path.join(dirpath, f)
                apply_to_name(data, f)
                if path.isfile(f):
                    apply_to_contents(data, f)
