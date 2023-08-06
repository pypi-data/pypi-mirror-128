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
Contains various helper functions related to the getML engine.
"""

import json
import socket

import getml.communication as comm

# --------------------------------------------------------------------


def delete_project(name):
    """Deletes a project.

    Args:
        name (str):
            Name of your project.

    Note:
        All data and models contained in the project directory will be
        permanently lost.

    """
    comm._delete_project(name)


# -----------------------------------------------------------------------------


def is_engine_alive():
    """Checks if the getML engine is running.

    Returns:
        bool:
            True if the getML engine is running and ready to accept
            commands and False otherwise.

    """

    # ---------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "is_alive"
    cmd["name_"] = ""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect(("localhost", comm.port))
    except ConnectionRefusedError:
        return False

    comm.send_string(sock, json.dumps(cmd))

    sock.close()

    return True


# define compatability alias
is_alive = is_engine_alive

# -----------------------------------------------------------------------------


def list_projects():
    """
    List all projects on the getML engine.

    Returns:
        List[str]:
            Lists the name all of the projects.
    """
    return comm._list_projects_impl(running_only=False)


# -----------------------------------------------------------------------------


def list_running_projects():
    """
    List all projects on the getML engine that are currently running.

    Returns:
        List[str]: Lists the name all of the projects currently running.
    """
    return comm._list_projects_impl(running_only=True)


# -----------------------------------------------------------------------------


def set_project(name):
    """Creates a new project or loads an existing one.

    If there is no project called `name` present on the engine, a new one will
    be created.

    Args:
        name (str):
            Name of the new project.
    """
    comm._set_project(name)


# -----------------------------------------------------------------------------


def shutdown():
    """Shuts down the getML engine.

    Note:
        All changes applied to the :class:`~getml.DataFrame`
        after calling their :meth:`~getml.DataFrame.save`
        method will be lost.

    """
    comm._shutdown()


# --------------------------------------------------------------------


def suspend_project(name):
    """Suspends a project that is currently running.

    Args:
        name (str):
            Name of your project.
    """
    comm._suspend_project(name)


# -----------------------------------------------------------------------------
