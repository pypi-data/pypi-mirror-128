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
Generates random numbers
"""

import numbers

from .columns import FloatColumnView


def random(seed=5849):
    """
    Create random column.

    The numbers will uniformly distributed from 0.0 to 1.0. This can be
    used to randomly split a population table into a training and a test
    set

    Args:
        seed (int):
            Seed used for the random number generator.

    Returns:
        :class:`~getml.data.columns.FloatColumnView`:
            FloatColumn containing random numbers

    Example:

        .. code-block:: python

            population = getml.DataFrame('population')
            population.add(numpy.zeros(100), 'column_01')

            idx = random(seed=42)
            population_train = population[idx > 0.7]
            population_test = population[idx <= 0.7]
    """

    if not isinstance(seed, numbers.Real):
        raise TypeError("'seed' must be a real number")

    col = FloatColumnView(operator="random", operand1=None, operand2=None)
    col.cmd["seed_"] = seed
    return col
