# basement

Basement is an extensible little tool for generating Python project scaffolding
based on mustache templates and common data you provide in a config file. It's
super straightforward.

## Installation

```
pip install basement
```

Not much more to say!

## Some Assembly Required (Usage)

Basement ships with two commands, `basement` and `ment`. `ment` is a shorthand
for `basement` and thus is exactly the same.

Some assembly is required, and you'll have to break out a screwdriver. Basement
is mostly useful because you can customize it! You can add your own templates
(which we will go over in the next section) as well as configure filler data for
all templates. We'll go over data the built in templates can make use of, as
well as what the built in templates are.

### Built In Templates

Basement comes with two built in templates:

* `default`: the default template (as you may have guessed) that is used when
  you don't specify a different one.
* `app`: a template defining a skeleton project using `click` to make a simple
  program with a command line interface.

You specify which template to use with the `-t` flag.

```
ment foo -t app
```

The above example would use the `app` template to generate the `foo` project.

### DATA

Templates aren't terribly useful until you fill them up with filler
data. Basement uses a [toml](https://github.com/toml-lang/toml) configuration
file to define this data. Create a file called `~/.basement` containing
something like the following:

```toml
full-name = "Anthony Grimes"
email = "anemail@raynes.me"
github-user = "Raynes"
license = "MIT"
```

Let's take a look at a file in the default template. This is `setup.py`:

```python
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
```

Notice all the `{{}}` things (mustaches)? These are mustache artifacts. When you
create a project based on this template, those will be mapped to keys in your
configuration file and filled in with the data present there. If I render based
on my config file, I get this:

```
Anthony@lastlight:~/code/basement (master *)
$ ment foobar
Rendered template 'default' at /Users/Anthony/code/basement/foobar
Anthony@lastlight:~/code/basement (master *)
$ cat foobar/setup.py
"""Your project's description"""
from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='foobar',
    description="A project that does things!",
    version='0.1.0',
    long_description=__doc__,
    packages=['foobar'],
    author='Anthony Grimes',
    author_email='anemail@raynes.me',
    url='https://github.com/Raynes/foobar',
    license='MIT',
    install_requires=requirements
)
```

#### Ignoring Files

Sometimes you don't want to touch certain files, in particular binary
files. `pystache`, the library basement uses to render mustache templates, often
does not like being fed binary files and you most certainly don't want huge
files to be read into memory to be rendered! For these situations, basement
provides a flexible mechanism for ignoring files. It works like so:

```
pass = ['path/to/be/ignored/.*']
```

`pass` can appear in your configuration and as each file is rendered, it is
checked against the regular expressions using Python's `re.search` function. If
any of the patterns match that file path, it is ignored and simply passed through.

## Creating Templates

Basement is designed so you can create your own templates really easily. All you
have to do is create a directory in `~/.basement-templates` where all templates
are stored and simply fill it with whatever files and content that you want,
adding mustaches wherever you want to fill in data from your config.

One thing to note is that `project-name` is filled in with the basename of the
output path you give basement. So if you run `ment path/to/project`, your
`project-name` will be `project`.

### Template-Specific Configuration

You can add configuration specifically for certain templates and any keys
present there that are also present at the top level override the top-level
keys. You simply use toml sections like so:

```toml
full-name = "Anthony Grimes"
email = "anemail@raynes.me"
github-user = "Raynes"
license = "MIT"

[app]
license = "EPL"
```

Given this configuration, when you create a project based on the `app` template,
`license` mustaches will be set to `EPL` rather than `MIT`. You can add
configuration specific to your own templates by doing the same thing, simply
adding sections with the name of the templates.

## Updating Basement

When you decide to update your basement (perhaps you want to add a pool table),
there are some updating mechanisms in place. When you run basement, it _always_
wipes its templates and re-adds them. This means that you *cannot* make changes
to the built in templates. If you want to make changes, you should make a new
template. 
