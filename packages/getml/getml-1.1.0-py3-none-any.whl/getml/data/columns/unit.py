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
The unit of this column.
"""

import getml.communication as comm

from .constants import VIEW_SIGNIFIER


@property  # type: ignore
def _unit(self):
    """
    The unit of this column.

    Units are used to determine which columns can be compared to each other
    by the feature learning algorithms.
    """

    # -------------------------------------------

    cmd = dict()

    cmd["name_"] = ""
    cmd["type_"] = (self.cmd["type_"] + ".get_unit").replace(VIEW_SIGNIFIER, "")

    cmd["col_"] = self.cmd

    # -------------------------------------------

    sock = comm.send_and_get_socket(cmd)

    # -------------------------------------------

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    unit = comm.recv_string(sock)

    return unit
