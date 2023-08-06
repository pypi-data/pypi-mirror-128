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
Returns a table as a list of lists.
"""

import sqlite3

# ----------------------------------------------------------------------------


def _handle_query(query):
    if "SELECT" in query:
        return query
    return 'SELECT * FROM "' + query + '";'


# ----------------------------------------------------------------------------


def to_list(conn, query):
    """
    Transforms a query or table into a list of lists. Returns
    a tuple which contains the column names and the actual data.

    Args:
        conn:
            A sqlite3 connection created by :func:`~getml.sqlite3.connect`.

        query (str):
            The query used to get the table. You can also
            pass the name of the table, in which case the entire
            table will be imported.
    """
    # ------------------------------------------------------------

    if not isinstance(conn, sqlite3.Connection):
        raise TypeError("'conn' must be an sqlite3.Connection object")

    if not isinstance(query, str):
        raise TypeError("'query' must be a str")

    # ------------------------------------------------------------

    query = _handle_query(query)
    cursor = conn.execute(query)
    colnames = [description[0] for description in cursor.description]
    data = cursor.fetchall()
    return colnames, data
