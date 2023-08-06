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
Contains the quantile aggregations.
"""

import numpy as np

from .helpers import _not_null

# ----------------------------------------------------------------------------


class _Quantile:
    def __init__(self, quantile):
        self.quantile = quantile
        self.values = []

    def step(self, value):
        """
        Executed every time the function is called.
        """
        if _not_null(value):
            self.values.append(value)

    def finalize(self):
        """
        Executed after all values are inserted.
        """
        return np.quantile(self.values, self.quantile, interpolation="linear")


# ----------------------------------------------------------------------------


class _Q1(_Quantile):
    def __init__(self):
        super().__init__(0.01)


# ----------------------------------------------------------------------------


class _Q5(_Quantile):
    def __init__(self):
        super().__init__(0.05)


# ----------------------------------------------------------------------------


class _Q10(_Quantile):
    def __init__(self):
        super().__init__(0.1)


# ----------------------------------------------------------------------------


class _Q25(_Quantile):
    def __init__(self):
        super().__init__(0.25)


# ----------------------------------------------------------------------------


class _Q75(_Quantile):
    def __init__(self):
        super().__init__(0.75)


# ----------------------------------------------------------------------------


class _Q90(_Quantile):
    def __init__(self):
        super().__init__(0.90)


# ----------------------------------------------------------------------------


class _Q95(_Quantile):
    def __init__(self):
        super().__init__(0.95)


# ----------------------------------------------------------------------------


class _Q99(_Quantile):
    def __init__(self):
        super().__init__(0.99)


# ----------------------------------------------------------------------------
