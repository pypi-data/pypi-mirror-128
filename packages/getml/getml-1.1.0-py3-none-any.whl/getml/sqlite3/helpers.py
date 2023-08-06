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
Contains simple helper functions for the sqlite3 module
"""

import logging
from inspect import cleandoc

import numpy as np

# ----------------------------------------------------------------------------


def _create_table(conn, table_name, schema, if_exists="append"):
    if _table_exists(conn, table_name):
        if if_exists == "fail":
            raise ValueError(f"Table {table_name} already exists!")
        if if_exists == "replace":
            conn.executescript(schema)
        elif if_exists == "append":
            _log("Appending...")
        else:
            raise TypeError(
                "`if_exists` has to be one of: 'append', 'replace', or 'fail'."
            )
    else:
        conn.executescript(schema)


# ----------------------------------------------------------------------------


def _generate_schema(name, sql_types):

    cols = []

    max_width = max(
        len(str(cname)) for cnames in sql_types.values() for cname in cnames
    )

    for type_, colnames in sql_types.items():
        colnames = [f'"{name}"' for name in colnames]
        cols.extend([f"{name:{max_width+2}} {type_}" for name in colnames])

    col_lines = ",\n    ".join(cols)

    template = cleandoc(
        """
        DROP TABLE IF EXISTS "{name}";

        CREATE TABLE "{name}" (
            {col_lines}
        );
        """
    )

    return template.format(name=name, col_lines=col_lines)


# ----------------------------------------------------------------------------


def _get_colnames(conn, table_name):
    cursor = conn.execute('SELECT * FROM "' + table_name + '" LIMIT 0')
    names = [description[0] for description in cursor.description]
    return names


# ----------------------------------------------------------------------------


def _get_num_columns(conn, table_name):
    return len(_get_colnames(conn, table_name))


# ----------------------------------------------------------------------------


def _is_int_type(coltype):
    return coltype in [
        int,
        np.int_,
        np.int8,
        np.int16,
        np.int32,
        np.int64,
        np.uint8,
        np.uint16,
        np.uint32,
        np.uint64,
    ]


# ----------------------------------------------------------------------------


def _log(msg):
    logging.basicConfig(format="%(asctime)s %(message)s", level=logging.INFO)
    logging.info(msg)


# ----------------------------------------------------------------------------


def _not_null(value):
    return value is not None and not np.isnan(value) and not np.isinf(value)


# ----------------------------------------------------------------------------


def _table_exists(conn, table_name):
    query = (
        f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    )

    cursor = conn.execute(query)

    if cursor.fetchone():
        return True
    return False


# ----------------------------------------------------------------------------
