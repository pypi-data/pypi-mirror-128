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

"""Helps you split data into a training, testing, validation or other sets.

Examples:
    Split at random:

    .. code-block:: python

        split = getml.data.split.random(
            train=0.8, test=0.1, validation=0.1
        )

        train_set = data_frame[split=='train']
        validation_set = data_frame[split=='validation']
        test_set = data_frame[split=='test']

    Split over time:

    .. code-block:: python

        validation_begin = getml.data.time.datetime(2010, 1, 1)
        test_begin = getml.data.time.datetime(2011, 1, 1)

        split = getml.data.split.time(
            population=data_frame,
            time_stamp="ds",
            test=test_begin,
            validation=validation_begin
        )

        # Contains all data before 2010-01-01 (not included)
        train_set = data_frame[split=='train']

        # Contains all data between 2010-01-01 (included) and 2011-01-01 (not included)
        validation_set = data_frame[split=='validation']

        # Contains all data after 2011-01-01 (included)
        test_set = data_frame[split=='test']
"""

from .concat import concat
from .random import random
from .time import time

__all__ = ("concat", "random", "time")
