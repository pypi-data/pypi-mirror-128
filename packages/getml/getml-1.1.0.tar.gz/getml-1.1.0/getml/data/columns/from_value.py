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
Generates an appropriate column from a value.
"""

import numbers

from .columns import FloatColumnView, StringColumnView, BooleanColumnView, _value_to_cmd

# -----------------------------------------------------------------------------


def from_value(val):
    """
    Creates a infinite column that contains the same
    value in all of its elements.

    val (bool, str or number):
        The value you want to insert into your column.
    """
    cmd = _value_to_cmd(val)

    if isinstance(val, bool):
        col = BooleanColumnView(
            operator="const",
            operand1=None,
            operand2=None,
        )
        col.cmd = cmd
        return col

    if isinstance(val, str):
        col = StringColumnView(
            operator="const",
            operand1=val,
            operand2=None,
        )
        col.cmd = cmd
        return col

    if isinstance(val, numbers.Number):
        col = FloatColumnView(
            operator="const",
            operand1=val,
            operand2=None,
        )
        col.cmd = cmd
        return col

    raise TypeError("val must be bool, str or a number.")
    return None
