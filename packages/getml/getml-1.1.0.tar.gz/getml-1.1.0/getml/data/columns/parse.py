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

"""Parses the columns from a cmd"""

from .constants import (
    BOOLEAN_COLUMN_VIEW,
    FLOAT_COLUMN,
    FLOAT_COLUMN_VIEW,
    STRING_COLUMN,
    STRING_COLUMN_VIEW,
)
from .columns import (
    FloatColumn,
    StringColumn,
    FloatColumnView,
    StringColumnView,
    BooleanColumnView,
)


def _make_column(cmd, Coltype):
    col = Coltype("", None, None)
    col.cmd = cmd
    return col


def _parse(cmd):
    typ = cmd["type_"]

    if typ == BOOLEAN_COLUMN_VIEW:
        return _make_column(cmd, BooleanColumnView)

    if typ == FLOAT_COLUMN:
        return _make_column(cmd, FloatColumn)

    if typ == FLOAT_COLUMN_VIEW:
        return _make_column(cmd, FloatColumnView)

    if typ == STRING_COLUMN:
        return _make_column(cmd, StringColumn)

    if typ == STRING_COLUMN_VIEW:
        return _make_column(cmd, StringColumnView)

    raise ValueError("Unknown column type: '" + typ + "'")
