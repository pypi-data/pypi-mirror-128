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
Transform column to a pyarrow.ChunkedArray
"""


import os
from typing import Any, Dict

import numpy as np
import pyarrow as pa  # type: ignore

import getml.communication as comm
from getml.database.helpers import _retrieve_temp_dir


def _to_arrow(self: Any, unique: bool = False) -> pa.ChunkedArray:
    """
    Transform column to numpy array
    """

    # -------------------------------------------

    typename = type(self).__name__.replace("View", "")

    # -------------------------------------------

    cmd: Dict[str, Any] = {}

    cmd["name_"] = ""
    cmd["type_"] = typename + (".unique" if unique else ".get")

    cmd["col_"] = self.cmd

    # -------------------------------------------

    sock = comm.send_and_get_socket(cmd)

    # -------------------------------------------

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)

    # -------------------------------------------

    with sock.makefile(mode="rb") as stream:
        with pa.ipc.open_stream(stream) as reader:
            return reader.read_all()["column"]

    # -------------------------------------------
