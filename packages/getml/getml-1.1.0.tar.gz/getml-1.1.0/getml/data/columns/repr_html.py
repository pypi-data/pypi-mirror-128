"""
HTML represenation of the column.
"""


def _repr_html(self):
    formatted = self._format()
    footer = self._collect_footer_data()
    return formatted._render_html(footer=footer)
