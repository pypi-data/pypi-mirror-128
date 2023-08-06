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
Copies a table from one database connection to another.
"""


import getml.communication as comm


def copy_table(source_conn, target_conn, source_table, target_table=None):
    """
    Copies a table from one database connection to another.

    Example:
        A frequent use case for this function is to copy data from a data source into
        sqlite. This is a good idea, because sqlite is faster than most standard,
        ACID-compliant databases and also you want to avoid messing up a productive
        environment.

        It is important to explicitly pass conn_id, otherwise the source connection
        will be closed
        when you create the target connection. What you pass as conn_id is entirely
        up to you,
        as long as the conn_id of the source and the target are different. It can
        be any name you see fit.

        >>> source_conn = getml.database.connect_odbc(
        ...     "MY-SERVER-NAME", conn_id="MY-SOURCE")
        >>>
        >>> target_conn = getml.database.connect_sqlite3(
        ...     "MY-SQLITE.db", conn_id="MY-TARGET")
        >>>
        >>> data.database.copy_table(
        ...         source_conn=source_conn,
        ...         target_conn=target_conn,
        ...         source_table="MY-TABLE"
        ... )

    Args:
        source_conn (:class:`~getml.database.Connection`):
            The database connection to be copied from.

        target_conn (:class:`~getml.database.Connection`):
            The database connection to be copied to.

        source_table (str):
            The name of the table in the source connection.

        target_table (str, optional):
            The name of the table in the target
            connection. If you do not explicitly pass a target_table, the
            name will be identical to the source_table.

    """

    # -------------------------------------------

    target_table = target_table or source_table

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Database.copy_table"

    cmd["source_conn_id_"] = source_conn.conn_id
    cmd["target_conn_id_"] = target_conn.conn_id
    cmd["source_table_"] = source_table
    cmd["target_table_"] = target_table

    # -------------------------------------------
    # Send JSON command to engine.

    comm.send(cmd)
