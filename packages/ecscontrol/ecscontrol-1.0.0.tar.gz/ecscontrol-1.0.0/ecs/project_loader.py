from .exceptions import InvalidProjectStructure, InvalidInputFiles
import os
import itertools
from ecs import render

def verify_input_file(p):
    # path does not have even a value
    if not p:
        raise FileNotFoundError

    # p has a value but it is not a path
    if not os.path.exists(p):
        raise FileNotFoundError

    # If p is a directory and contains no files
    if os.path.isdir(p):
        os.listdir(p)

    # Return value if complies
    return p


def _find_td_ser(project_path, tp="task-definition"):
    """
    Function identifying task-definition within a project directory. The
    exps variable define order/priority for selection of task-definition
    """
    e = [".yml", ".yaml", ".json", "/"]
    exps = ["{}{}".format(tp, x) for x in e]

    # Generate paths
    paths = [os.path.join(project_path, x) for x in exps]

    # Find the first matching file/dir
    for p in paths:
        try:
           verify_input_file(p)
           return p
        except FileNotFoundError as e:
            pass
    
    # Raise exception if no such file is in the project directory
    raise FileNotFoundError


def _find_values(project_path):
    """
    This function identifies values used for tempalte interpolation within
    the values.yml of values/default.yml/yaml/json file.
    """

    # Define potential sources
    exts = ["yml", "yaml", "json"]
    file_names  = ["values", "values/default"]
    
    # Iterate
    for fn in file_names:
        p = itertools.product([fn], exts)
        paths = [os.path.join(project_path, "{}.{}".format(*x)) for x in p]

        for path in paths:
            try:
                verify_input_file(path)
                return [path]
            except FileNotFoundError as e:
                pass

    # Raise exception if no such file is in the project directory
    raise FileNotFoundError
    

def load_project_files(project_path="ecs/", values=None):
    # Find task-definition.yml/json/yaml or task-definition/
    try:
        td = _find_td_ser(project_path)
    except FileNotFoundError as e:
        raise InvalidProjectStructure("Unable to find task-definition")

    # Find service.yml/json/yaml or service/
    try:
        service = _find_td_ser(project_path, tp="service")
    except FileNotFoundError as e:
        raise InvalidProjectStructure("Unable to find service definition")

    # if values == None then look for values.yml/yaml/json
    if values is None or (values.__class__ == list and len(values) == 0):
        try:
            values = _find_values(project_path)
        except FileNotFoundError as e:
            raise InvalidProjectStructure("Unable to find values for interpolation")
    else:
        # Deal with project files loading
        if values.__class__ != list:
            raise Exception('Invalid input variable values. Expecting list type!')
        
        # Lets validate input list
        ep = [os.path.exists(x) for x in values]
        if not all(ep):
            raise InvalidInputFiles

    # Return clean paths to task-definition and value files
    return (td, service, values)


def _load_and_interpolate_values(values, envs):
    # Load values from files
    rvalues = [render.load_path(x) for x in values]
    rvalues = [item for sublist in rvalues for item in sublist]
    values = render.merge_dicts(rvalues)

    # Override values from envs dict
    if not envs.__class__ is dict:
        raise Exception('Envs variable must be dict!')
    values = render.merge_dicts([values, envs])

    # Append extra variables
    values['region'] = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

    # Interpolate variables
    if len(values):
        # Return interpolated values
        return render.interpolate_values(values)
    
    # Return values
    return values


def load_project(project_path, values, envs):
    # Load files
    ftd, fservice, fvalues = load_project_files(project_path, values)

    # Load values
    ivalues = _load_and_interpolate_values(fvalues, envs)
    
    # Load task definition
    td = render.load_path(ftd, ivalues)
    mtd = render.merge_dicts(td)

    # Load service definition
    service = render.load_path(fservice, ivalues)
    mservice = render.merge_dicts(service)

    # Load output definition
    try: 
        output = load_output(project_path, values, envs)
    except FileNotFoundError as e:
        output = ""

    # Return generates descriptors
    return mtd, mservice, output


def load_output(project_path, values, envs):
    # The output file name is given
    fn = os.path.join(project_path, 'output.j2')

    # If exists then load otherwise return blank output
    if verify_input_file(fn):
        ivalues = _load_and_interpolate_values(values, envs)
        p = render.load_path(fn, ivalues, raw=True)
        return '\n'.join(p).strip()
    else:
        return ""