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
Displays a View.
"""

from copy import deepcopy
from inspect import cleandoc

from ..templates import environment
from .data_frame_formatter import (
    _DataFrameFormatColumn,
    _DataFrameFormatter,
    _structure_subroles,
)
from .helpers import _get_view_content

# -----------------------------------------------------------------------------


class _ViewFormatter(_DataFrameFormatter):

    max_rows = _DataFrameFormatter.max_rows // 2

    template = environment.get_template("column.jinja2")

    # ------------------------------------------------------------

    def __init__(self, view, num_head=max_rows):

        self.colnames = view.colnames

        nrows_is_known = not isinstance(view.nrows(), str)

        self.n_rows = int(view.nrows()) if nrows_is_known else None

        if self.n_rows:
            num_head = min(num_head, self.n_rows)

        cols = [view[colname].cmd for colname in view.colnames]
        roles = [view.roles.infer(colname) for colname in view.colnames]
        units = [view[colname].unit for colname in view.colnames]

        self.units = None

        self.subroles = {
            cat: subroles
            for cat, subroles in _structure_subroles(view).items()
            if any(subrole for subrole in subroles)
        }

        rows = _get_view_content(start=0, length=num_head, cols=cols)["data"]

        columns = [list(col) for col in zip(*rows)]

        headers = [self.colnames] + [roles]

        if any(unit != "" for unit in units):
            self.units = units
            headers += [units]

        if self.subroles:
            headers += [[""] * len(columns)] + [
                subroles
                for subroles in self.subroles.values()
                if any(subrole for subrole in subroles)
            ]

        headers = list(zip(*headers))

        self.data = [
            _ViewFormatColumn(
                headers=list(header),
                cells=cells,
                max_cells=self.max_rows,
                n_cells=self.n_rows,
                role=role,
            )
            for header, role, cells in zip(headers, roles, columns)
        ]

        index_headers = ["name"]
        if self.roles:
            index_headers += ["role"]
        if self.units:
            index_headers += ["unit"]
        if self.subroles:
            index_headers += ["subroles:"] + [f"- {cat:7}" for cat in self.subroles]

        self._add_index(index_headers)

    # ------------------------------------------------------------

    def _add_index(self, headers):
        index_column = _ViewFormatColumn(
            headers=headers,
            cells=list(range(len(self.data[0]))),
            max_cells=self.max_rows,
            n_cells=self.n_rows,
        )

        self.data = [index_column] + self.data

    # ------------------------------------------------------------

    def _render_footer_lines(self, footer):
        footer_lines = cleandoc(
            f"""
            {footer.n_rows} rows x {footer.n_cols} columns
            type: {footer.type}
            """
        )

        return footer_lines


# -----------------------------------------------------------------------------


class _ViewFormatColumn(_DataFrameFormatColumn):
    """"""

    def _clip(self):
        ellipses = "..." + getattr(self, "precision", 0) * " "
        column_clipped = deepcopy(self)
        if not self.n_cells or self.n_cells > self.max_cells:
            ellipses = [self.header_template.format(ellipses)]
            if self.nested:
                ellipses = [ellipses]
            column_clipped.data += ellipses
            return column_clipped
        return column_clipped
