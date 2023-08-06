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

"""Base object not meant to be called directly."""

import getml.communication as comm


class _Column:
    """
    Base object not meant to be called directly.
    """

    # -------------------------------------------------------------------------

    def __init__(self):
        self.cmd = dict()

    # ------------------------------------------------------------

    @property
    def _monitor_url(self):
        """
        The URL of the column.
        """
        return (
            comm._monitor_url()
            + "getcolumn/"
            + comm._get_project_name()
            + "/"
            + self.cmd["df_name_"]
            + "/"
            + self.name
            + "/"
        )

    # ------------------------------------------------------------

    @property
    def name(self):
        """
        The role of this column.
        """
        return self.cmd["name_"]

    # -------------------------------------------------------------------------

    @property
    def role(self):
        """
        The role of this column.

        Roles are needed by the feature learning algorithm so it knows how
        to treat the columns.
        """
        return self.cmd["role_"]
