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
Concatenates data.
"""

from getml.data.columns import StringColumnView
from getml.data.columns.from_value import from_value
from getml.data.columns.columns import rowid
from getml.data.concat import concat as _concat
from getml.data.data_frame import DataFrame
from getml.data.helpers import _is_non_empty_typed_list
from getml.data.view import View


def concat(name, **kwargs):
    """
    Concatenates several data frames into and produces a split
    column that keeps track of their origin.

    Args:
        name (str):
            The name of the data frame you would like to create.

        kwargs:
            The data frames you would like
            to concat with the name in which they should appear
            in the split column.

    Example:
        A common use case for this functionality are :class:`~getml.data.TimeSeries`:

        .. code-block:: python

            data_train = getml.DataFrame.from_pandas(
                datatraining_pandas, name='data_train')

            data_validate = getml.DataFrame.from_pandas(
                datatest_pandas, name='data_validate')

            data_test = getml.DataFrame.from_pandas(
                datatest2_pandas, name='data_test')

            population, split = getml.data.split.concat(
                "population", train=data_train, validate=data_validate, test=data_test)

            ...

            time_series = getml.data.TimeSeries(
                population=population, split=split)

            my_pipeline.fit(time_series.train)
    """

    if not _is_non_empty_typed_list(list(kwargs.values()), [DataFrame, View]):
        raise ValueError(
            "'kwargs' must be non-empty and contain getml.DataFrames "
            + "or getml.data.Views."
        )

    names = list(kwargs.keys())

    first = kwargs[names[0]]

    population = first.copy(name) if isinstance(first, DataFrame) else first.to_df(name)

    split = from_value(names[0])

    assert isinstance(split, StringColumnView), "Should be a StringColumnView"

    for new_df_name in names[1:]:
        split = split.update(rowid() > population.nrows(), new_df_name)
        population = _concat(name, [population, kwargs[new_df_name]])

    return population, split[: population.nrows()]
