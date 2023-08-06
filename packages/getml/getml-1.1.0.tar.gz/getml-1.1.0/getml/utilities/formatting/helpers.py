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
Collection of helper functions that are not intended to be used by
the end-user.
"""

import json

import getml.communication as comm

# --------------------------------------------------------------------


def _get_column_content(col, coltype, start, length):
    """
    Returns the contents of a data frame in a format that is
    compatible with jquery.data.tables.

    Args:
        col (dict): The cmd describing the dict.

        coltype (str): The type of the column
            (FloatColumn, StringColumn or BooleanColumn).

        start (int): The number of the first line to retrieve.

        length (int): The number of lines to retrieve.
    """

    # ------------------------------------------------------------

    if not isinstance(start, int):
        raise TypeError("'start' must be an int.")

    if not isinstance(length, int):
        raise TypeError("'length' must be an int.")

    # ------------------------------------------------------------

    cmd = dict()

    cmd["type_"] = coltype + ".get_content"
    cmd["name_"] = ""

    cmd["col_"] = col
    cmd["draw_"] = 1

    cmd["start_"] = start
    cmd["length_"] = length

    # ------------------------------------------------------------

    sock = comm.send_and_get_socket(cmd)

    json_str = comm.recv_string(sock)

    if json_str[0] != "{":
        comm.engine_exception_handler(json_str)

    # ------------------------------------------------------------

    return json.loads(json_str)


# --------------------------------------------------------------------


def _get_data_frame_content(name, start, length):
    """
    Returns the contents of a data frame in a format that is
    compatible with jquery.data.tables.

    Args:
        name (str): The name of the data frame.

        start (int): The number of the first line to retrieve.

        length (int): The number of lines to retrieve.
    """

    # ------------------------------------------------------------

    if not isinstance(name, str):
        raise TypeError("'name' must be a str.")

    if not isinstance(start, int):
        raise TypeError("'start' must be an int.")

    if not isinstance(start, int):
        raise TypeError("'length' must be an int.")

    # ------------------------------------------------------------

    cmd = dict()

    cmd["type_"] = "DataFrame.get_content"
    cmd["name_"] = name

    cmd["start_"] = start
    cmd["length_"] = length

    cmd["draw_"] = 1

    # ------------------------------------------------------------

    sock = comm.send_and_get_socket(cmd)

    json_str = comm.recv_string(sock)

    if json_str[0] != "{":
        comm.engine_exception_handler(json_str)

    # ------------------------------------------------------------

    return json.loads(json_str)


# --------------------------------------------------------------------


def _get_view_content(start, length, cols):

    # ------------------------------------------------------------

    cmd = dict()

    cmd["type_"] = "View.get_content"
    cmd["name_"] = ""

    cmd["start_"] = start
    cmd["length_"] = length
    cmd["cols_"] = cols

    cmd["draw_"] = 1

    # ------------------------------------------------------------

    sock = comm.send_and_get_socket(cmd)

    json_str = comm.recv_string(sock)

    if json_str[0] != "{":
        comm.engine_exception_handler(json_str)

    # ------------------------------------------------------------

    return json.loads(json_str)
