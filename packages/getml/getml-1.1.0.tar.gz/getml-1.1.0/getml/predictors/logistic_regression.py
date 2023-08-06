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
A simple logistic regression model for predicting classification problems.
"""

from dataclasses import dataclass

from .linear_regression import _validate_linear_model_parameters
from .predictor import _Predictor

# ------------------------------------------------------------------------------


@dataclass(repr=False)
class LogisticRegression(_Predictor):
    """Simple predictor for classification problems.

    Learns a simple linear relationship using the sigmoid function:

    .. math::

        \\hat{y} = \\sigma(w_0 + w_1 * feature_1 + w_2 * feature_2 + ...)

    :math:`\\sigma` denotes the sigmoid function:

    .. math::

        \\sigma(z) = \\frac{1}{1 + exp(-z)}

    The weights are optimized by minimizing the cross entropy loss of
    the predictions :math:`\\hat{y}` w.r.t. the :ref:`targets
    <annotating_roles_target>` :math:`y`.

    .. math::

        L(\\hat{y},y) = - y*\\log \\hat{y} - (1 - y)*\\log(1 - \\hat{y})

    Logistic regressions are always trained numerically.

    If you decide to pass :ref:`categorical
    features<annotating_roles_categorical>` to the
    :class:`~getml.predictors.LogisticRegression`, it will be trained
    using the Broyden-Fletcher-Goldfarb-Shannon (BFGS) algorithm.
    Otherwise, it will be trained using adaptive moments (Adam). BFGS
    is more accurate, but less scalable than Adam.

    Args:
        learning_rate (float, optional):
            The learning rate used for the Adaptive Moments algorithm
            (only relevant when categorical features are
            included). Range: (0, :math:`\\infty`]

        reg_lambda (float, optional):
            L2 regularization parameter. Range: [0, :math:`\\infty`]

    """

    # ----------------------------------------------------------------

    learning_rate: float = 0.9
    reg_lambda: float = 1e-10

    # ----------------------------------------------------------------

    def validate(self, params=None):
        """Checks both the types and the values of all instance
        variables and raises an exception if something is off.

        Args:
            params (dict, optional): A dictionary containing
                the parameters to validate. If not is passed,
                the own parameters will be validated.

        Examples:

            .. code-block:: python

                l = getml.predictors.LogisticRegression()
                l.learning_rate = 20
                l.validate()

        Note:

            This method is called at end of the __init__ constructor
            and every time before the predictor - or a class holding
            it as an instance variable - is send to the getML engine.
        """

        if params is None:
            params = self.__dict__
        else:
            params = {**self.__dict__, **params}

        if not isinstance(params, dict):
            raise ValueError("params must be None or a dictionary!")

        _validate_linear_model_parameters(params)


# ------------------------------------------------------------------------------
