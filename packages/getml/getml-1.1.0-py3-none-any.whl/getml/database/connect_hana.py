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
Creates a new HANA database connection.
"""

import getml.communication as comm
import getml.constants as constants

from .connection import Connection


def connect_hana(
    user,
    password,
    host,
    port=39017,
    default_schema="public",
    ping_interval=0,
    time_formats=None,
    conn_id="default",
):
    """
    Creates a new HANA database connection.

    Args:
        user (str):
            User name with which to log into the HANA database.

        password (str):
            Password with which to log into the HANA database.

        host (str):
            Host of the HANA database.

        port (int, optional):
            Port of the database.

        default_schema (str, optional):
            The schema within the database you want to connect
            use unless another schema is explicitly set.

        ping_interval (int, optional):
            The interval at which you want to ping the database,
            in seconds. Set to 0 for no pings at all.

        time_formats (List[str], optional):
            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

        conn_id (str, optional):
            The name to be used to reference the connection.
            If you do not pass anything, this will create a new default connection.

    Note:
        By selecting an existing table of your database in
        :func:`~getml.DataFrame.from_db` function, you can create
        a new :class:`~getml.DataFrame` containing all its data.
        Alternatively you can use the
        :meth:`~.getml.DataFrame.read_db` and
        :meth:`~.getml.DataFrame.read_query` methods to replace
        the content of the current :class:`~getml.DataFrame`
        instance or append further rows based on either a table or a
        specific query.

        You can also write your results back into the MySQL
        database. By passing the name for the destination table to
        :meth:`getml.Pipeline.transform`, the features
        generated from your raw data will be written back. Passing
        them into :meth:`getml.Pipeline.predict`, instead,
        makes predictions of the target variables to new, unseen data
        and stores the result into the corresponding table.

    """
    # -------------------------------------------

    time_formats = time_formats or constants.TIME_FORMATS

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = "Database.new"
    cmd["db_"] = "sap_hana"

    cmd["host_"] = host
    cmd["port_"] = port
    cmd["default_schema_"] = default_schema
    cmd["user_"] = user
    cmd["ping_interval_"] = ping_interval
    cmd["time_formats_"] = time_formats
    cmd["conn_id_"] = conn_id

    # -------------------------------------------
    # Send JSON command to engine.

    sock = comm.send_and_get_socket(cmd)

    # -------------------------------------------
    # The password is sent separately, so it doesn't
    # end up in the logs.

    comm.send_string(sock, password)

    # -------------------------------------------
    # Make sure that everything went well.

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    return Connection(conn_id=conn_id)
