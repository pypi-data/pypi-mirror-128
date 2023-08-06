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

"""This module contains machine learning algorithms to learn and predict on the
generated features.

The predictor classes defined in this module serve two
purposes. First, a predictor can be used as a ``feature_selector``
in :class:`~getml.Pipeline` to only select the best features
generated during the automated feature learning and to get rid off
any redundancies. Second, by using it as a ``predictor``, it will
be trained on the features of the supplied data set and used to
predict to unknown results. Every time a new data set is passed to
the :meth:`~getml.Pipeline.predict` method of one of the
:mod:`~getml.models`, the raw relational data is interpreted in the
data model, which was provided during the construction of the model,
transformed into features using the trained feature learning
algorithm, and, finally, its :ref:`target<annotating_roles_target>`
will be predicted using the trained predictor.

The algorithms can be grouped according to their finesse and
whether you want to use them for a classification or
regression problem.

.. csv-table::

    "", "simple", "sophisticated"
    "regression", ":class:`~getml.predictors.LinearRegression`", ":class:`~getml.predictors.XGBoostRegressor`"
    "classification", ":class:`~getml.predictors.LogisticRegression`", ":class:`~getml.predictors.XGBoostClassifier`"

Note:

    All predictors need to be passed to :class:`~getml.Pipeline`.
"""

# ------------------------------------------------------------------------------

from .linear_regression import LinearRegression
from .logistic_regression import LogisticRegression
from .predictor import _Predictor
from .xgboost_classifier import XGBoostClassifier
from .xgboost_regressor import XGBoostRegressor

# ------------------------------------------------------------------------------


__all__ = (
    "LinearRegression",
    "LogisticRegression",
    "XGBoostClassifier",
    "XGBoostRegressor",
)

# ------------------------------------------------------------------------------

_classification_types = [LogisticRegression().type, XGBoostClassifier().type]

# ------------------------------------------------------------------------------
