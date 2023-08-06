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
Subset class intended to be passed to the pipeline.
"""

from dataclasses import dataclass
from inspect import cleandoc
from typing import Dict, Union

from getml.utilities.formatting import _Formatter

from .data_frame import DataFrame
from .view import View


@dataclass
class Subset:
    """
    A Subset consists of a population table and one or several peripheral tables.

    It is passed by a :class:`~getml.data.Container`, :class:`~getml.data.StarSchema`
    and :class:`~getml.data.TimeSeries` to the :class:`~getml.Pipeline`.

    Example:
        .. code-block:: python

            container = getml.data.Container(
                train=population_train,
                test=population_test
            )

            container.add(
                meta=meta,
                order=order,
                trans=trans
            )

            # train and test are Subsets.
            # They contain population_train
            # and population_test respectively,
            # as well as ther peripheral tables
            # meta, order and trans.
            my_pipeline.fit(container.train)

            my_pipeline.score(container.test)
    """

    container_id: str
    peripheral: Dict[str, Union[DataFrame, View]]
    population: Union[DataFrame, View]

    def _format(self):
        headers_perph = [["name", "rows", "type"]]

        rows_perph = [
            [perph.name, perph.nrows(), type(perph).__name__]
            for perph in self.peripheral.values()
        ]

        names = [perph.name for perph in self.peripheral.values()]
        aliases = list(self.peripheral.keys())

        if any(alias not in names for alias in aliases):
            headers_perph[0].insert(0, "alias")

            for alias, row in zip(aliases, rows_perph):
                row.insert(0, alias)

        return self.population._format(), _Formatter(
            headers=headers_perph, rows=rows_perph
        )

    def __repr__(self):
        pop, perph = self._format()
        pop_footer = self.population._collect_footer_data()

        template = cleandoc(
            """
            population
            {pop}

            peripheral
            {perph}
            """
        )

        return template.format(
            pop=pop._render_string(footer=pop_footer), perph=perph._render_string()
        )

    def _repr_html_(self):
        pop, perph = self._format()
        pop_footer = self.population._collect_footer_data()

        template = cleandoc(
            """
            <div>
                <h4>population</h4>
                {pop}
            </div>
            <div>
                <h4>peripheral</h4>
                {perph}
            </div>
            """
        )

        return template.format(
            pop=pop._render_html(footer=pop_footer), perph=perph._render_html()
        )
