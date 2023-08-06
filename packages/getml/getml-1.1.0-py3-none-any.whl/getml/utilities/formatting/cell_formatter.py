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

import string


class CellFormatter(string.Formatter):
    """
    Custom formatter for cells in output columns. Supports all python-native format specs
    (https://docs.python.org/3/library/string.html#formatspec) plus the following custom
    format specs:
       - <w_idth>.<p_recision>fd (float): like <w>.<p>f, but the values of a column are
         decimal point aligned
       - <w_idth>.<p_recision>d (str): formats strings (holdings numbers) in a column on
         the decimal point by taking into account the precision
    """

    integer_overhang = 1

    # ------------------------------------------------------------

    def format_field(self, value, format_spec):

        if format_spec.endswith("fd"):
            return self._format_float_decimal_point(value, format_spec)

        if format_spec.endswith("d"):
            return self._format_string_decimal_point(value, format_spec)

        return super().format_field(value, format_spec)

    # ------------------------------------------------------------

    def _format_float_decimal_point(self, value, format_spec):
        width = int(format_spec.split(".")[0].strip())
        precision = int(format_spec.split(".")[1][0])
        padding = precision - self.integer_overhang

        if value.is_integer():
            formatted = f"{value:{width-padding}.{self.integer_overhang}f}"
            # fix misalignment due to missing decimal point
            if self.integer_overhang == 0:
                formatted = formatted[1:]
            return f"{formatted:{width}}"

        formatted = super().format_field(value, format_spec[:-1])
        stripped = formatted.rstrip("0")
        return f"{stripped:{width}}"

    # ------------------------------------------------------------

    def _format_string_decimal_point(self, value, format_spec):
        width = int(format_spec.split(".")[0].strip())
        precision = int(format_spec.split(".")[1][0])

        if value.strip("-").isdigit() or value == "nan":
            formatted = f"{value:>{width-precision-1}}"
            return f"{formatted:{width}}"

        if "." in value:
            digits = len(value.split(".")[1])
        else:
            digits = 0
        formatted = f"{value:>{width-precision+digits}}"
        return f"{formatted:{width}}"
