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

"""Collects the data necessary for displaying the column footer."""

from collections import namedtuple

from .constants import _views


def _collect_footer_data(self):
    if type(self).__name__ in _views:
        footer = namedtuple("footer", ["n_rows", "type"])
        nrows_is_known = not isinstance(self.length, str)

        return footer(
            n_rows=self.length if nrows_is_known else self.length + " number of ",
            type=type(self).__name__,
        )

    footer = namedtuple("footer", ["n_rows", "data_frame", "type", "url"])

    return footer(
        n_rows=len(self),
        data_frame=self.cmd["df_name_"] if "df_name_" in self.cmd else "",
        type=type(self).__name__,
        url=self._monitor_url,
    )
