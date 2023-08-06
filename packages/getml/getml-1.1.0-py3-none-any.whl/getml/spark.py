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
This module is useful for productionizing pipelines
on Apache Spark.
"""

import os

from getml.sqlite3.helpers import _log
from getml.sqlite3.execute import _retrieve_scripts


def execute(spark, fname):
    """
    Executes an SQL script or several SQL scripts on Spark.

    Args:
        spark (pyspark.sql.session.SparkSession):
            The spark session.

        fname (str):
            The names of the SQL script or a folder containing SQL scripts.
            If you decide to pass a folder, the SQL scripts must have the ending '.sql'.
    """
    # ------------------------------------------------------------

    if not isinstance(fname, str):
        raise TypeError("'fname' must be of type str")

    # ------------------------------------------------------------

    if os.path.isdir(fname):
        scripts = _retrieve_scripts(fname, ".sql")
        for script in scripts:
            execute(spark, script)
        return

    # ------------------------------------------------------------

    _log("Executing " + fname + "...")

    queries = open(fname, "rt").read()
    queries = queries.split(";")
    for query in queries:
        if query.strip():
            spark.sql(query)
