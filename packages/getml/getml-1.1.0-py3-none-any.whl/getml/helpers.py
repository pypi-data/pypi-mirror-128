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
Collection of helper classes that are relevant
for many submodules.
"""

# --------------------------------------------------------------------


def _check_parameter_bounds(parameter, parameter_name, bounds):
    """Checks whether a particular parameter does lie within the provided
    `bounds`.

    Args:
        parameter (numeric): Particular value of an instance variable.
        key_name (string): Name of the parameter used for an
            expressive Exception
        bounds (list[numeric]): Numerical list of length 2
            specifying the lower and upper bound (in that order)
            of `parameter`.
    """
    if parameter < bounds[0] or parameter > bounds[1]:
        raise ValueError(
            "'"
            + parameter_name
            + "' is only defined for range ["
            + str(bounds[0])
            + ", "
            + str(bounds[1])
            + "]"
        )
