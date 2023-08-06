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
Executes SQL scripts on SQLite3
"""

import os
import sqlite3

import numpy as np

from .helpers import _log

# ----------------------------------------------------------------------------


def _retrieve_scripts(folder, file_type):
    if folder[-1] != "/":
        folder = folder + "/"
    scripts = os.listdir(folder)
    scripts = [script for script in scripts if script[-len(file_type) :] == file_type]
    scripts = [folder + script for script in scripts]
    scripts = np.asarray(scripts)
    scripts.sort()
    return scripts


# ----------------------------------------------------------------------------


def execute(conn, fname):
    """
    Executes an SQL script or several SQL scripts on SQLite3.

    Args:
        conn (sqlite3.Connection):
            A sqlite3 connection created by :func:`~getml.sqlite3.connect`.

        fname (str):
            The names of the SQL script or a folder containing SQL scripts.
            If you decide to pass a folder, the SQL scripts must have the ending '.sql'.
    """
    # ------------------------------------------------------------

    if not isinstance(conn, sqlite3.Connection):
        raise TypeError("'conn' must be an sqlite3.Connection object")

    if not isinstance(fname, str):
        raise TypeError("'fname' must be of type str")

    # ------------------------------------------------------------

    # Store temporary object in-memory.
    conn.execute("PRAGMA temp_store=2;")

    if os.path.isdir(fname):
        scripts = _retrieve_scripts(fname, ".sql")
        for script in scripts:
            execute(conn, script)
        return

    _log("Executing " + fname + "...")

    queries = open(fname, "rt").read()
    queries = queries.split(";")
    for query in queries:
        conn.execute(query + ";")

    conn.commit()


# ----------------------------------------------------------------------------
