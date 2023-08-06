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
Reads data into an sqlite3 table.
"""

import sqlite3

from .helpers import _get_num_columns, _log


def read_list(conn, table_name, data):
    """
    Reads data into an sqlite3 table.

    Args:
        conn:
            A sqlite3 connection created by :func:`~getml.sqlite3.connect`.

        table_name (str):
            The name of the table to write to.

        data (List[List[Object]]):
            The data to insert into the table.
            Every list represents one row to be read into the table.
    """

    # ------------------------------------------------------------

    if not isinstance(conn, sqlite3.Connection):
        raise TypeError("'conn' must be an sqlite3.Connection object")

    if not isinstance(table_name, str):
        raise TypeError("'table_name' must be a string")

    if not isinstance(data, list):
        raise TypeError("'data' must be a list of lists")

    # ------------------------------------------------------------

    ncols = _get_num_columns(conn, table_name)
    old_length = len(data)
    data = [line for line in data if len(line) == ncols]
    placeholders = "(" + ",".join(["?"] * ncols) + ")"
    query = 'INSERT INTO "' + table_name + '" VALUES ' + placeholders
    conn.executemany(query, data)
    conn.commit()
    _log(
        "Read "
        + str(len(data))
        + " lines. "
        + str(old_length - len(data))
        + " invalid lines."
    )
