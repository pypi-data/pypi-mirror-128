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

"""This module contains all possible aggregations to be used with
:class:`~getml.feature_learning.Multirel`,
:class:`~getml.feature_learning.FastProp`,
:class:`~getml.preprocessors.Mapping`.


Refer to the :ref:`feature learning section in the user guide
<feature_learning_design>` for details about how
these aggregations are used in the context of feature learning.

"""

from collections import namedtuple

# ------------------------------------------------------------------------------

Avg = "AVG"
"""Average value of a given numerical column.
"""

Count = "COUNT"
"""Number of rows in a given column.
"""

CountAboveMean = "COUNT ABOVE MEAN"
"""Counts the number of values strictly greater than the mean.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

CountBelowMean = "COUNT BELOW MEAN"
"""Counts the number of values strictly smaller than the mean.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

CountDistinct = "COUNT DISTINCT"
"""Count function with distinct clause. This only counts unique elements."""

CountDistinctOverCount = "COUNT DISTINCT OVER COUNT"
"""COUNT DISTINCT divided by COUNT.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

CountMinusCountDistinct = "COUNT MINUS COUNT DISTINCT"
"""Counts minus counts distinct. Substracts COUNT DISTINCT from COUNT.
"""

EWMA_1s = "EWMA_1S"
"""Exponentially weighted moving average with an half-life of 1 second.
"""

EWMA_1m = "EWMA_1M"
"""Exponentially weighted moving average with an half-life of 1 minute.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

EWMA_1h = "EWMA_1H"
"""Exponentially weighted moving average with an half-life of 1 hour.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

EWMA_1d = "EWMA_1D"
"""Exponentially weighted moving average with an half-life of 1 day.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

EWMA_7d = "EWMA_7D"
"""Exponentially weighted moving average with an half-life of 7 days.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

EWMA_30d = "EWMA_30D"
"""Exponentially weighted moving average with an half-life of 30 days.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

EWMA_90d = "EWMA_90D"
"""Exponentially weighted moving average with an half-life of 90 days.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

EWMA_365d = "EWMA_365D"
"""Exponentially weighted moving average with an half-life of 365 days.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

First = "FIRST"
"""First value of a given column, when ordered by the time stamp.
"""

Kurtosis = "KURTOSIS"
"""The kurtosis of a given column.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Last = "LAST"
"""Last value of a given column, when ordered by the time stamp.
"""

Max = "MAX"
"""Largest value of a given column.
"""

Median = "MEDIAN"
"""Median of a given column
"""

Min = "MIN"
"""Smallest value of a given column.
"""

Mode = "MODE"
"""Most frequent value of a given column.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

NumMax = "NUM MAX"
"""The number of times we observe the maximum value.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

NumMin = "NUM MIN"
"""The number of times we observe the minimum value.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Q1 = "Q1"
"""The 1%-quantile.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Q5 = "Q5"
"""The 5%-quantile.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Q10 = "Q10"
"""The 10%-quantile.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Q25 = "Q25"
"""The 25%-quantile.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Q75 = "Q75"
"""The 75%-quantile.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Q90 = "Q90"
"""The 90%-quantile.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Q95 = "Q95"
"""The 95%-quantile.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Q99 = "Q99"
"""The 99%-quantile.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Skew = "SKEW"
"""Skewness of a given column.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Stddev = "STDDEV"
"""Standard deviation of a given column.
"""

Sum = "SUM"
"""Total sum of a given numerical column.
"""

TimeSinceFirstMaximum = "TIME SINCE FIRST MAXIMUM"
"""The time difference between the first time we see
the maximum value and the time stamp in the population
table. If the maximum value is unique, then TIME SINCE
FIRST MAXIMUM and TIME SINCE LAST MAXIMUM are identical.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

TimeSinceFirstMinimum = "TIME SINCE FIRST MINIMUM"
"""The time difference between the first time we see
the minimum value and the time stamp in the population
table. If the minimum value is unique, then TIME SINCE
FIRST MINIMUM and TIME SINCE LAST MINIMUM are identical.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

TimeSinceLastMaximum = "TIME SINCE LAST MAXIMUM"
"""The time difference between the last time we see
the maximum value and the time stamp in the population
table. If the maximum value is unique, then TIME SINCE
FIRST MAXIMUM and TIME SINCE LAST MAXIMUM are identical.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

TimeSinceLastMinimum = "TIME SINCE LAST MINIMUM"
"""The time difference between the last time we see
the minimum value and the time stamp in the population
table. If the minimum value is unique, then TIME SINCE
FIRST MINIMUM and TIME SINCE LAST MINIMUM are identical.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Trend = "TREND"
"""Extracts a linear trend from a variable over time and
extrapolates this trend to the current time stamp.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

Var = "VAR"
"""Statistical variance of a given numerical column.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

VariationCoefficient = "VARIATION COEFFICIENT"
"""VAR divided by MEAN.
Please note that this aggregation is
not supported by
:class:`~getml.feature_learning.Multirel`.
"""

# ------------------------------------------------------------------------------

_multirel_subset = [
    Avg,
    Count,
    CountDistinct,
    CountMinusCountDistinct,
    First,
    Last,
    Max,
    Median,
    Min,
    Stddev,
    Sum,
    Var,
]


# ------------------------------------------------------------------------------

_additional_aggregations_for_fast_prop = [
    CountAboveMean,
    CountBelowMean,
    CountDistinctOverCount,
    EWMA_1s,
    EWMA_1m,
    EWMA_1h,
    EWMA_1d,
    EWMA_7d,
    EWMA_30d,
    EWMA_90d,
    EWMA_365d,
    Kurtosis,
    Mode,
    NumMax,
    NumMin,
    Q1,
    Q5,
    Q10,
    Q25,
    Q75,
    Q90,
    Q95,
    Q99,
    Skew,
    TimeSinceFirstMaximum,
    TimeSinceFirstMinimum,
    TimeSinceLastMaximum,
    TimeSinceLastMinimum,
    Trend,
    VariationCoefficient,
]

# ------------------------------------------------------------------------------

_mapping_subset = [
    Avg,
    Count,
    CountAboveMean,
    CountBelowMean,
    CountDistinct,
    CountDistinctOverCount,
    CountMinusCountDistinct,
    Kurtosis,
    Max,
    Median,
    Min,
    Mode,
    NumMax,
    NumMin,
    Q1,
    Q5,
    Q10,
    Q25,
    Q75,
    Q90,
    Q95,
    Q99,
    Skew,
    Stddev,
    Sum,
    Var,
    VariationCoefficient,
]

# ------------------------------------------------------------------------------

_all_aggregations = _multirel_subset + _additional_aggregations_for_fast_prop

# ------------------------------------------------------------------------------

_Aggregations = namedtuple("_Aggregations", ["All", "Default", "Minimal"])

# ------------------------------------------------------------------------------

fastprop = _Aggregations(
    All=_all_aggregations,
    Default=[
        Avg,
        Count,
        CountDistinct,
        CountMinusCountDistinct,
        First,
        Last,
        Max,
        Median,
        Min,
        Mode,
        Stddev,
        Sum,
        Trend,
    ],
    Minimal=[Avg, Count, Max, Min, Sum],
)
"""
Set of default aggregations for :class:`~getml.feature_learning.FastProp` and
:class:`~getml.feature_learning.FastPropTimeseries`. `All` contains all aggregations
supported by FastProp, `Default` contains the subset of reasonable default aggregations,
`Minimal` is minimal set.
"""

# ------------------------------------------------------------------------------

mapping = _Aggregations(
    All=_mapping_subset,
    Default=[Avg],
    Minimal=[Avg],
)
"""
Set of default aggregations for :class:`~getml.preprocessor.Mapping`. `All` contains all
aggregations supported by the mapping preprocessor. `Default` and `Minimal` are identical
and include only the AVG aggregation, which is the recommended setting for classification
problems.
"""

# ------------------------------------------------------------------------------

multirel = _Aggregations(
    All=_multirel_subset,
    Default=[
        Avg,
        Count,
        Max,
        Min,
        Sum,
    ],
    Minimal=[Avg, Count, Sum],
)
"""
Set of default aggregations for :class:`~getml.feature_learning.Multirel`.
`All` contains all aggregations
supported by Multirel, `Default` contains the subset of reasonable default aggregations,
`Minimal` is minimal set.
"""

# --------------------------------------------------------------------
