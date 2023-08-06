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

from getml.data.columns import FloatColumn, FloatColumnView, StringColumnView
from getml.data.columns.from_value import from_value
from getml.data.data_frame import DataFrame
from getml.data.helpers import _is_typed_list
from getml.data.view import View


def time(population, time_stamp, validation=None, test=None, **kwargs):
    """
    Returns a :class:`~getml.data.columns.StringColumnView` that can be used to divide
    data into training, testing, validation or other sets.

    The arguments are
    :code:`key=value` pairs of names (:code:`key`) and starting points (:code:`value`).
    The starting point defines the left endpoint of the subset. Intervals are left
    closed and right open, such that :math:`[value, next value)`.  The (unnamed) subset
    left from the first named starting point, i.e.  :math:`[0, first value)`, is always
    considered to be the training set.

    Args:
        population (:class:`~getml.DataFrame` or :class:`~getml.data.View`):
            The population table you would like to split.

        time_stamp (str):
            The name of the time stamp column in the population table
            you want to use. Ideally, the role of said column would be
            :const:`~getml.data.roles.time_stamp`. If you want to split on the rowid,
            then pass "rowid" to `time_stamp`.

        validation (float, optional):
            The start date of the validation set.

        test (float, optional):
            The start date of the test set.

        kwargs (float, optional):
            Any other sets you would like to assign.
            You can name these sets whatever you want to (in our example,
            we called it 'other').

    Example:
        .. code-block:: python

            validation_begin = getml.data.time.datetime(2010, 1, 1)
            test_begin = getml.data.time.datetime(2011, 1, 1)
            other_begin = getml.data.time.datetime(2012, 1, 1)

            split = getml.data.split.time(
                population=data_frame,
                time_stamp="ds",
                test=test_begin,
                validation=validation_begin,
                other=other_begin
            )

            # Contains all data before 2010-01-01 (not included)
            train_set = data_frame[split=='train']

            # Contains all data between 2010-01-01 (included) and 2011-01-01 (not included)
            validation_set = data_frame[split=='validation']

            # Contains all data between 2011-01-01 (included) and 2012-01-01 (not included)
            test_set = data_frame[split=='test']

            # Contains all data after 2012-01-01 (included)
            other_set = data_frame[split=='other']
    """
    if not isinstance(population, (DataFrame, View)):
        raise ValueError("'population' must be a DataFrame or a View.")

    if not isinstance(time_stamp, (str, FloatColumn, FloatColumnView)):
        raise ValueError(
            "'time_stamp' must be a string, a FloatColumn, or a FloatColumnView."
        )

    if not test and not validation and not kwargs:
        raise ValueError("You have to supply at least one starting point.")

    defaults = {"test": test, "validation": validation}

    sets = {name: value for name, value in defaults.items() if value is not None}

    sets.update({**kwargs})

    values = np.asarray(list(sets.values()))
    index = np.argsort(values)
    values = values[index]

    if not _is_typed_list(values.tolist(), numbers.Real):
        raise ValueError("All values must be real numbers.")

    names = np.asarray(list(sets.keys()))
    names = names[index]

    if isinstance(time_stamp, str):
        time_stamp_col = (
            population[time_stamp] if time_stamp != "rowid" else population.rowid
        )
    else:
        time_stamp_col = time_stamp

    col = from_value("train")

    assert isinstance(col, StringColumnView), "Should be a StringColumnView"

    for i in range(len(names)):
        col = col.update(
            time_stamp_col >= values[i],
            names[i],
        )

    return col
