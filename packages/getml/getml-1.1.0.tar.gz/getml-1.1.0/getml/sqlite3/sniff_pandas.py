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
Contains utility functions for siffing sqlite data types from pandas DataFrames.
"""

import pandas as pd  # type: ignore

from getml.data.helpers import _is_numerical_type

from .helpers import _generate_schema, _is_int_type

# ----------------------------------------------------------------------------


def sniff_pandas(table_name, data_frame):
    """
    Sniffs a pandas data frame.

    Args:
        table_name (str):
            Name of the table in which the data is to be inserted.

        data_frame (pandas.DataFrame):
            The pandas.DataFrame to read into the table.

    Returns:
        str:
            Appropriate `CREATE TABLE` statement.
    """
    # ------------------------------------------------------------

    if not isinstance(table_name, str):
        raise TypeError("'table_name' must be a str")

    if not isinstance(data_frame, pd.DataFrame):
        raise TypeError("'data_frame' must be a pandas.DataFrame")

    # ------------------------------------------------------------

    colnames = data_frame.columns
    coltypes = data_frame.dtypes

    sql_types = dict(INTEGER=[], REAL=[], TEXT=[])

    for cname, ctype in zip(colnames, coltypes):
        if _is_int_type(ctype):
            sql_types["INTEGER"].append(cname)
            continue
        if _is_numerical_type(ctype):
            sql_types["REAL"].append(cname)
        else:
            sql_types["TEXT"].append(cname)

    return _generate_schema(table_name, sql_types)
