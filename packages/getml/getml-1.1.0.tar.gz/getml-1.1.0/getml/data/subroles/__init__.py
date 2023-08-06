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

"""Subroles allow for more fine-granular control of how certain columns
will be used by the pipeline.

A column can have no subrole, one subrole or several subroles.

Example:
    .. code-block:: python

        # The Relboost feature learning algorithm will
        # ignore this column.
        my_data_frame.set_subroles(
            "my_column", getml.data.subroles.exclude.relboost)

        # The Substring preprocessor will be applied to this column.
        # But other preprocessors, feature learners or predictors
        # are not excluded from using it as well.
        my_data_frame.set_subroles(
            "ucc", getml.data.subroles.include.substring)

        # Only the EmailDomain preprocessor will be applied
        # to "emails". All other preprocessors, feature learners,
        # feature selectors and predictors will ignore this column.
        my_data_frame.set_subroles("emails", getml.data.subroles.only.email)
"""

from .exclude import _all_exclude
from .include import _all_include
from .only import _all_only

_all_subroles = _all_exclude + _all_include + _all_only

__all__ = ("exclude", "include", "only")
