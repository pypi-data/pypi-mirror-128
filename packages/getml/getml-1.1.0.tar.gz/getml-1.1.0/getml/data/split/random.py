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
Splits data at random.
"""

import numbers

import numpy as np

from getml.data.columns import StringColumnView
from getml.data.columns import random as random_col
from getml.data.columns.from_value import from_value
from getml.data.helpers import _is_typed_list


def random(seed=5849, train=0.8, test=0.2, validation=0, **kwargs):
    """
    Returns a :class:`~getml.data.columns.StringColumnView` that
    can be used to randomly divide data into training, testing,
    validation or other sets.

    Args:
        seed (int):
            Seed used for the random number generator.

        train (float, optional):
            The share of random samples assigned to
            the training set.

        validation (float, optional):
            The share of random samples assigned to
            the validation set.

        test (float, optional):
            The share of random samples assigned to
            the test set.

        kwargs (float, optional):
            Any other sets you would like to assign.
            You can name these sets whatever you want to (in our example,
            we called it 'other').

    Example:
        .. code-block:: python

            split = getml.data.split.random(
                train=0.8, test=0.1, validation=0.05, other=0.05
            )

            train_set = data_frame[split=='train']
            validation_set = data_frame[split=='validation']
            test_set = data_frame[split=='test']
            other_set = data_frame[split=='other']

    """

    values = np.asarray([train, validation, test] + list(kwargs.values()))

    if not _is_typed_list(values.tolist(), numbers.Real):
        raise ValueError("All values must be real numbers.")

    if np.abs(np.sum(values) - 1.0) > 0.0001:
        raise ValueError(
            "'train', 'validation', 'test' and all other sets must add up to 1, "
            + "but add up to "
            + str(np.sum(values))
            + "."
        )

    upper_bounds = np.cumsum(values)
    lower_bounds = upper_bounds - values

    names = ["train", "validation", "test"] + list(kwargs.keys())

    col = from_value("train")

    assert isinstance(col, StringColumnView), "Should be a StringColumnView"

    for i in range(len(names)):
        col = col.update(
            (random_col(seed=seed) >= lower_bounds[i])
            & (random_col(seed=seed) < upper_bounds[i]),
            names[i],
        )

    return col
