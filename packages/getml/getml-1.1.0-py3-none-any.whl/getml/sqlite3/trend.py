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
Extracts linear trends over time.
"""

import numpy as np

from .helpers import _not_null

# ----------------------------------------------------------------------------


class _Trend:
    def __init__(self):
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
        if not self.values:
            return None
        mean_x = np.mean([v[0] for v in self.values])
        mean_y = np.mean([v[1] for v in self.values])
        sum_xx = np.sum([(v[0] - mean_x) * (v[0] - mean_x) for v in self.values])
        if sum_xx == 0.0:
            return mean_y
        sum_xy = np.sum([(v[0] - mean_x) * (v[1] - mean_y) for v in self.values])
        beta = sum_xy / sum_xx
        return mean_y - beta * mean_x


# ----------------------------------------------------------------------------
