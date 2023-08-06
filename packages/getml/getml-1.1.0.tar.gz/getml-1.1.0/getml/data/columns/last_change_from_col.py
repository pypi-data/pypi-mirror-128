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
The last time any of the underlying data frames has been changed.
"""

from .last_change import _last_change


@property  # type: ignore
def _last_change_from_col(self):
    """
    The last time any of the underlying data frames has been changed.
    """

    def _last_change_from_cmd(cmd):
        if cmd["type_"] == "FloatColumn" or cmd["type_"] == "StringColumn":
            assert "df_name_" in cmd, "Expected df_name_"
            return _last_change(cmd["df_name_"])

        def get_operand(op):
            return [_last_change_from_cmd(cmd[op])] if op in cmd else []

        all_values = (
            [""]
            + get_operand("operand1_")
            + get_operand("operand2_")
            + get_operand("condition_")
        )

        return max(all_values)

    return _last_change_from_cmd(self.cmd)
