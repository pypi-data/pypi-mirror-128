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
Sniffs a list of CSV files.
"""


import getml.communication as comm

from .connection import Connection
from .helpers import _retrieve_urls


def sniff_csv(
    name,
    fnames,
    num_lines_sniffed=1000,
    quotechar='"',
    sep=",",
    skip=0,
    colnames=None,
    conn=None,
):
    """
    Sniffs a list of CSV files.

    Args:
        name (str):
            Name of the table in which the data is to be inserted.

        fnames (List[str]):
            The list of CSV file names to be read.

        num_lines_sniffed (int, optional):
            Number of lines analyzed by the sniffer.

        quotechar (str, optional):
            The character used to wrap strings. Default:`"`

        sep (str, optional):
            The separator used for separating fields. Default:`,`

        skip (int, optional):
            Number of lines to skip at the beginning of each
            file (Default: 0).

        colnames(List[str] or None, optional):
            The first line of a CSV file
            usually contains the column names. When this is not the case, you need to
            explicitly pass them.

        conn (:class:`~getml.database.Connection`, optional):
            The database connection to be used.
            If you don't explicitly pass a connection,
            the engine will use the default connection.

    Returns:
        str: Appropriate `CREATE TABLE` statement.
    """
    # -------------------------------------------

    conn = conn or Connection()

    # -------------------------------------------

    if not isinstance(fnames, list):
        fnames = [fnames]

    fnames_ = _retrieve_urls(fnames)

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = name
    cmd["type_"] = "Database.sniff_csv"

    cmd["fnames_"] = fnames_
    cmd["num_lines_sniffed_"] = num_lines_sniffed
    cmd["quotechar_"] = quotechar
    cmd["sep_"] = sep
    cmd["skip_"] = skip
    cmd["conn_id_"] = conn.conn_id

    if colnames is not None:
        cmd["colnames_"] = colnames

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_get_socket(cmd)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        sock.close()
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    stmt = comm.recv_string(sock)

    sock.close()

    return stmt
