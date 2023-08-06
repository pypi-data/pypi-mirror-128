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
Contains the exponentially weighted moving average aggregations.
"""

import numpy as np

from .helpers import _not_null

# ----------------------------------------------------------------------------


class _EWMA:
    log05 = np.log(0.5)

    t1s = 1.0
    t1m = t1s * 60.0
    t1h = t1m * 60.0
    t1d = t1h * 24.0
    t7d = t1d * 7.0
    t30d = t1d * 30.0
    t90d = t1d * 90.0
    t365d = t1d * 365.0

    def __init__(self, half_life):
        self.half_life = half_life
        self.values = []

    def step(self, value, time_stamp):
        """
        Executed every time the function is called.
        """
        if _not_null(value):
            self.values.append((time_stamp, value))

    def finalize(self):
        """
        Executed after all values are inserted.
        """
        weights = [np.exp(_EWMA.log05 * v[0] / self.half_life) for v in self.values]
        sum_weights = np.sum(weights)
        if sum_weights == 0.0:
            return None
        sum_all = np.dot([v[1] for v in self.values], weights)
        return sum_all / sum_weights


# ----------------------------------------------------------------------------


class _EWMA1S(_EWMA):
    def __init__(self):
        super().__init__(_EWMA.t1s)


# ----------------------------------------------------------------------------


class _EWMA1M(_EWMA):
    def __init__(self):
        super().__init__(_EWMA.t1m)


# ----------------------------------------------------------------------------


class _EWMA1H(_EWMA):
    def __init__(self):
        super().__init__(_EWMA.t1h)


# ----------------------------------------------------------------------------


class _EWMA1D(_EWMA):
    def __init__(self):
        super().__init__(_EWMA.t1d)


# ----------------------------------------------------------------------------


class _EWMA7D(_EWMA):
    def __init__(self):
        super().__init__(_EWMA.t7d)


# ----------------------------------------------------------------------------


class _EWMA30D(_EWMA):
    def __init__(self):
        super().__init__(_EWMA.t30d)


# ----------------------------------------------------------------------------


class _EWMA90D(_EWMA):
    def __init__(self):
        super().__init__(_EWMA.t90d)


# ----------------------------------------------------------------------------


class _EWMA365D(_EWMA):
    def __init__(self):
        super().__init__(_EWMA.t365d)


# ----------------------------------------------------------------------------
