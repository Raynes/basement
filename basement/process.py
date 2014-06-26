import os
from os import path
from shutil import copytree
from pprint import pprint
import re

from pystache import render

from basement import config


class AlreadyExistsError(Exception):
    pass


def apply_to_name(data, name):
    """Rename a file assumed to have a mustache template
    in its name to the name with the template rendered.

    """
    old_path, base = path.split(name)
    new_path = path.join(old_path, render(base, data))
    base, ext = path.splitext(new_path)
    out = base if ext == '.basement-ignore' else new_path
    os.rename(name, out)
    return out


def apply_to_contents(data, name):
    """Render a template file, replacing it in place.

    """
    with open(name, 'r+') as f:
        contents = f.read()
        f.seek(0)
        f.write(render(contents, data))
        f.truncate()


def should_pass(f, patterns):
    """Checks f against pass patterns to see if we should copy
    f unchanged.

    """
    patterns.append('basement-ignore$')
    for pattern in patterns:
        pattern = re.compile(pattern)
        if pattern.search(f):
            return True
    return False


def process(template, output, verbose=False):
    """Process a template directory, creating our final output"""
    if path.exists(output):
        raise AlreadyExistsError("Output path already exists!")
    else:
        data = config.template_config(template)
        data['project-name'] = path.basename(output)
        pass_patterns = data.get('pass', [])
        if verbose:
            print("Data is:")
            pprint(data)
        copytree(config.lookup_template(template), output)
        for dirpath, directories, files in os.walk(output, topdown=False):
            for f in files + directories:
                f = path.join(dirpath, f)
                new_f = apply_to_name(data, f)
                if path.isfile(new_f):
                    if not should_pass(f, pass_patterns):
                        apply_to_contents(data, new_f)
