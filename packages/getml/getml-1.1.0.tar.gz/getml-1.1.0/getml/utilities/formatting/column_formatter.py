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
Displays a column
"""

from inspect import cleandoc

from ..templates import environment
from .data_frame_formatter import (
    _DataFrameFormatColumn,
    _DataFrameFormatter,
    _get_subroles,
)
from .helpers import _get_column_content

# -----------------------------------------------------------------------------


class _ColumnFormatter(_DataFrameFormatter):

    max_rows = _DataFrameFormatter.max_rows

    template = environment.get_template("column.jinja2")

    # ------------------------------------------------------------

    def __init__(self, col, num_head=max_rows // 2, num_tail=max_rows // 2):
        self.coltype = type(col).__name__

        self.name = getattr(col, "name", None)
        self.role = getattr(col, "role", None)

        self.unit = getattr(col, "unit", None)
        self.subroles = {
            cat: subroles for cat, subroles in _get_subroles(col).items() if subroles
        }

        nrows_is_known = not isinstance(col.length, str)

        self.n_rows = int(col.length) if nrows_is_known else None

        num_head = min(num_head, self.n_rows or self.max_rows // 2 + 1)
        num_tail = min(num_tail, self.n_rows or self.max_rows // 2)

        head = _get_column_content(
            col=col.cmd,
            coltype=self.coltype.replace("View", ""),
            start=0,
            length=num_head,
        )["data"]

        tail = (
            _get_column_content(
                col=col.cmd,
                coltype=self.coltype.replace("View", ""),
                start=int(self.n_rows - num_tail),
                length=num_tail,
            )["data"]
            if "View" not in self.coltype
            else []
        )

        cells = [cell[0] for cell in head + tail]

        header = [self.name or ""]

        if self.role:
            header += [self.role]

        if self.unit:
            header += [self.unit]

        if self.subroles:
            header += [""] + [
                subroles
                for subroles in self.subroles.values()
                if any(subrole for subrole in subroles)
            ]

        self.data = [
            _DataFrameFormatColumn(
                headers=list(header),
                cells=cells,
                max_cells=self.max_rows,
                n_cells=self.n_rows,
                role=self.role,
            )
        ]

        index_headers = ["name" if self.name else ""]
        if self.role:
            index_headers += ["role"]
        if self.unit:
            index_headers += ["unit"]
        if self.subroles:
            index_headers += ["subroles:"] + [f"- {cat:7}" for cat in self.subroles]

        self._add_index(index_headers)

        if "View" in self.coltype:
            self.max_rows = num_head

    # ------------------------------------------------------------

    def _render_footer_lines(self, footer):
        footer_lines = cleandoc(
            f"""
            {footer.n_rows} rows
            type: {footer.type}
            """
        )

        if "View" not in self.coltype:
            footer_lines += f"\nurl: {footer.url}"

        return footer_lines

    # ------------------------------------------------------------

    def _render_body(self, as_html=False):
        return super(_ColumnFormatter, self)._render_body(as_html)
