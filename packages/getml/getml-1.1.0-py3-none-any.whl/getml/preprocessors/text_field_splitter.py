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
Contains routines for preprocessing data frames.
"""

from dataclasses import dataclass

from .preprocessor import _Preprocessor
from .validate import _validate


# NOTE: The r at the beginning of the docstring
# is necessary to correctly display the characters.
# https://docutils.sourceforge.io/docs/ref/rst/directives.html#code
@dataclass(repr=False)
class TextFieldSplitter(_Preprocessor):
    r"""
    A TextFieldSplitter splits columns with role :const:`getml.data.roles.text`
    into relational bag-of-words representations to allow the
    feature learners to learn patterns based on
    the prescence of certain words within the text fields.

    Text fields will be splitted on a whitespace or any of the
    following characters:

    .. code:: python

        ; , . ! ? - | " \t \v \f \r \n % ' ( ) [ ] { }

    Refer to the :ref:`User guide <text_fields>` for more information.

    Example:
        .. code-block:: python

            text_field_splitter = getml.preprocessors.TextFieldSplitter()

            pipe = getml.Pipeline(
                population=population_placeholder,
                peripheral=[order_placeholder, trans_placeholder],
                preprocessors=[text_field_splitter],
                feature_learners=[feature_learner_1, feature_learner_2],
                feature_selectors=feature_selector,
                predictors=predictor,
                share_selected_features=0.5
            )
    """

    def validate(self, params=None):
        """Checks both the types and the values of all instance
        variables and raises an exception if something is off.

        Args:
            params (dict, optional):
                A dictionary containing
                the parameters to validate. If not is passed,
                the own parameters will be validated.
        """
        _validate(self, params)
