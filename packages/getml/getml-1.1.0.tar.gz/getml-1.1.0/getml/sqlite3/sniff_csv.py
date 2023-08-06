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
Contains utility functions for siffing sqlite data types from CSV files.
"""

import pandas as pd  # type: ignore

from getml.data.helpers import _is_typed_list, _is_non_empty_typed_list

from .sniff_pandas import sniff_pandas

# ----------------------------------------------------------------------------


def sniff_csv(
    fnames,
    table_name,
    header=True,
    num_lines_sniffed=1000,
    quotechar='"',
    sep=",",
    skip=0,
    colnames=None,
):
    """
    Sniffs a list of csv files.

    Args:
        fnames (List[str]):
            The list of CSV file names to be read.

        table_name (str):
            Name of the table in which the data is to be inserted.

        header (bool):
            Whether the csv file contains a header. If True, the first line
            is skipped and column names are inferred accordingly.

        num_lines_sniffed (int, optional):
            Number of lines analyzed by the sniffer.

        quotechar (str, optional):
            The character used to wrap strings. Default:`"`

        sep (str, optional):
            The separator used for separating fields. Default:`,`

        skip (int, optional):
            Number of lines to skip at the beginning of each
            file (Default: 0).

        colnames(List[str] or None, optional):
            The first line of a CSV file
            usually contains the column names. When this is not the case, you can
            explicitly pass them. If you pass colnames, it is assumed that the
            CSV files do not contain a header, thus overriding the 'header' variable.

    Returns:
        str:
            Appropriate `CREATE TABLE` statement.
    """

    # ------------------------------------------------------------

    if not isinstance(fnames, list):
        fnames = [fnames]

    # ------------------------------------------------------------

    if not _is_non_empty_typed_list(fnames, str):
        raise TypeError("'fnames' must be a string or a non-empty list of strings")

    if not isinstance(table_name, str):
        raise TypeError("'table_name' must be a string")

    if not isinstance(header, bool):
        raise TypeError("'header' must be a bool")

    if not isinstance(num_lines_sniffed, int):
        raise TypeError("'num_lines_sniffed' must be a int")

    if not isinstance(quotechar, str):
        raise TypeError("'quotechar' must be a str")

    if not isinstance(sep, str):
        raise TypeError("'sep' must be a str")

    if not isinstance(skip, int):
        raise TypeError("'skip' must be an int")

    if colnames is not None and not _is_typed_list(colnames, str):
        raise TypeError("'colnames' must be a list of strings or None")

    # ------------------------------------------------------------

    header_lines = 0 if header and not colnames else None

    def read(fname):
        return pd.read_csv(
            fname,
            nrows=num_lines_sniffed,
            header=header_lines,
            sep=sep,
            quotechar=quotechar,
            skiprows=skip,
            names=colnames,
        )

    data_frames = [read(fname) for fname in fnames]

    merged = pd.concat(data_frames, join="inner")

    return sniff_pandas(table_name, merged)
