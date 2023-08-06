# Copyright 2021 The SQLNet Company GmbH

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

"""
Handles access to project-related information.
"""

from sys import modules

import getml.communication as comm
from getml.engine import is_engine_alive, is_monitor_alive, list_projects

from .containers import DataFrames, Hyperopts, Pipelines

_functions = []

_props = []


def __getattr__(key):

    if key in _functions:
        return getattr(modules.get(__name__), key)

    if key in _props:
        if is_engine_alive():
            return getattr(modules.get(__name__), "_" + key)()
        elif is_monitor_alive():
            projects = "\n".join(list_projects())
            msg = comm._make_error_msg()
            msg += "\n\nAvailable projects:\n\n"
            msg += projects
            print(msg)
            return None
        else:
            msg = comm._make_error_msg()
            print(msg)
            return None

    raise AttributeError(f"module 'getml.project' has no attribute {key}")


def module_function(func):
    _functions.append(func.__name__)
    return func


def module_prop(prop):
    _props.append(prop.__name__[1:])
    return prop


@module_prop
def _data_frames():
    return DataFrames()


@module_prop
def _hyperopts():
    return Hyperopts()


@module_prop
def _pipelines():
    return Pipelines()


@module_prop
def _name():
    return comm._get_project_name()


@module_function
def load(bundle, name=None):
    """
    Loads a project from a bundle and connects to it.

    Args:
        bundle (str): The '.getml' bundle file to load.

        name (str): A name for the project contained in the bundle.
          If None, the name will be extracted from the bundle.
    """
    return comm._load_project(bundle, name)


@module_function
def delete():
    """
    Deletes the currently connected project. All related pipelines,
    data frames and hyperopts will be irretrivably deleted.
    """
    comm._delete_project(_name())


@module_function
def restart():
    """
    Suspends and then relaunches the currently connected project.
    This will kill all jobs currently running on that process.
    """
    comm._set_project(_name(), restart=True)


@module_function
def save(filename=None, target_dir=None, replace=True):
    """
    Saves the currently connected project to disk.

    Args:
        filename (str): The name of the '.getml' bundle file

        target_dir (str): the directory to save the bundle to.
          If None, the current working directory is used.

        replace (bool): Whether to replace an existing bundle.
    """
    return comm._save_project(_name(), filename, target_dir, replace)


@module_function
def suspend():
    """
    Suspends the currently connected project.
    """
    return comm._suspend_project(_name())


@module_function
def switch(name):
    """Creates a new project or loads an existing one.

    If there is no project called `name` present on the engine, a new one will
    be created. See the :ref:`User guide <project_management>` for more
    information.

    Args:
        name (str): Name of the new project.
    """
    comm._set_project(name)


_all = _functions + _props
