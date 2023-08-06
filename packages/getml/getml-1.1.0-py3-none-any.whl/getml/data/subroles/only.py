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
Columns marked with a subrole in this submodule will only be used
for the specified purpose and nothing else.

Example:
    .. code-block:: python

        # Only the EmailDomain preprocessor will be applied
        # to "emails". All other preprocessors, feature learners,
        # feature selectors and predictors will ignore this column.
        my_data_frame.set_subroles("emails", getml.data.subroles.only.email)
"""

email = "only email"
"""
A column with this subrole will only be
used for the :class:`~getml.preprocessors.EmailDomain`
preprocessor and nothing else. It will be ignored by all other preprocessors,
feature learners and predictors.
"""

substring = "only substring"
"""
A column with this subrole will only be
used for the :class:`~getml.preprocessors.Substring`
preprocessor and nothing else. It will be ignored by all other preprocessors,
feature learners and predictors.
"""

__all__ = ("email", "substring")

_all_only = [email, substring]
