import os
import errno
import magic
import yaml
from jinja2 import Template, Environment, FileSystemLoader
from .extra_filters import get_jira_id, get_slug, filter_dateparser, filter_format, decode_aws_secret


# support function allowing to read content of a file or directory specified by path variable
def load_path(path, ivalues=None, raw=False):

    # test if file even exists
    if not os.path.exists(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    # Load as a directory
    if os.path.isdir(path):
        vars = []
        for f in os.listdir(path):
            try:
                vars += load_path(os.path.join(path, f), ivalues)
            except Exception as e:
                # I particularly dont like this way, but it works..
                # TODO: should be modified, so an dedicated exception is raised
                if "Not a loadable yaml format" in str(e):
                    continue
                raise e
        return vars
    else:
        # print ("reading file")
        mime = magic.from_file(path, mime=True)
        if not mime in ["text/plain", "text/html", "application/json", "application/yaml"]:
            raise Exception("File {} is not in the text/plain format, but {}".format(path, mime))

        # Try to read yaml file
        with open(path, "r") as f:
            if not ivalues is None:
                # Interpolate the loaded file - this is most likely task_definition
                # That should be in Jinja2 format
                env = Environment()
                env.filters['jira_id'] = get_jira_id
                env.filters['slug'] = get_slug
                env.filters['dateparser'] = filter_dateparser
                env.filters['format_timestamp'] = filter_format
                env.filters['decode_aws_secret'] = decode_aws_secret
                env.loader = FileSystemLoader(os.path.dirname(path))
                t = env.from_string(f.read())
                r = t.render(**ivalues)
                if raw:
                    data = r
                else:
                    data = yaml.load(r, Loader=yaml.FullLoader)
            else:
                if raw:
                    data = f.read()
                else:
                    # Simply load the yaml/json - this should be file with values
                    data = yaml.load(f, Loader=yaml.FullLoader)
            if data.__class__.__name__ != 'dict' and not raw:
                raise Exception("Not a loadable yaml format - {}".format(path))
            return [data]


# This function will need to merge all loaded dicts
# At the moment, I will implemented very simple merge without deep nesting
# merging support.
def merge_dicts(list_of_dicts):
    _tmp = {}
    for d in list_of_dicts:
        _tmp = merge(_tmp, d)
    return _tmp


def merge(a, b, path=None):
    "merges b into a"
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif isinstance(a[key], list) and isinstance(b[key], list):
                a[key] += b[key]
            elif isinstance(a[key], str) and isinstance(b[key], str):
                a[key] = b[key]
            elif isinstance(a[key], int) and isinstance(b[key], int):
                a[key] = b[key]
            elif isinstance(a[key], float) and isinstance(b[key], float):
                a[key] = b[key]
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


# This is just a helping function mimicing Ansible's interpolation within variables
# I do not exepct anybody will ever need more than 5 consecutive interpolations
# if so it means there is a very bad pattern how deployment is configured
def interpolate_values(values):
    td = yaml.dump(values, Dumper=yaml.Dumper)
    for i in range(0, 5):
        template = Template(td)
        td = template.render(**values)
        if not "{{" in td:
            return yaml.load(td, Loader=yaml.FullLoader)
    raise Exception("Too many recusions")


# This function takes task_definition in the form of a dict and uses jinja2 for
# variable interplation using values which is another dict composed of all provided
# variables
def render(task_definition, values):
    td = yaml.dump(task_definition, Dumper=yaml.Dumper)
    template = Template(td)
    td = template.render(interpolate_values(values))
    return yaml.load(td, Loader=yaml.FullLoader)
