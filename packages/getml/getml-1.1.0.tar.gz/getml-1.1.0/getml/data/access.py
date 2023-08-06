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
Manages the access to various data sources.
"""

import getml.communication as comm
from getml.engine import is_alive as _is_alive

# -----------------------------------------------------------------------------


def set_s3_access_key_id(value):
    """Sets the Access Key ID to S3.

    NOTE THAT S3 IS NOT SUPPORTED ON WINDOWS.

    In order to retrieve data from S3, you need to set the Access Key ID
    and the Secret Access Key. You can either set them as environment
    variables before you start the getML engine or you can set them from
    this module.

    Args:
        value (str):
            The value to which you want to set the Access Key ID.
    """

    if not isinstance(value, str):
        raise TypeError("'value' must be of type str")

    if not _is_alive():
        raise ConnectionRefusedError(
            """
        Cannot connect to getML engine.
        Make sure the engine is running on port '"""
            + str(comm.port)
            + """' and you are logged in.
        See `help(getml.engine)`."""
        )

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "set_s3_access_key_id"
    cmd["name_"] = ""

    sock = comm.send_and_get_socket(cmd)

    comm.send_string(sock, value)

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)


# -----------------------------------------------------------------------------


def set_s3_secret_access_key(value):
    """Sets the Secret Access Key to S3.

    NOTE THAT S3 IS NOT SUPPORTED ON WINDOWS.

    In order to retrieve data from S3, you need to set the Access Key ID
    and the Secret Access Key. You can either set them as environment
    variables before you start the getML engine or you can set them from
    this module.

    Args:
        value (str):
            The value to which you want to set the Secret Access Key.
    """

    if not isinstance(value, str):
        raise TypeError("'value' must be of type str")

    if not _is_alive():
        raise ConnectionRefusedError(
            """
        Cannot connect to getML engine.
        Make sure the engine is running on port '"""
            + str(comm.port)
            + """' and you are logged in.
        See `help(getml.engine)`."""
        )

    # ----------------------------------------------------------------

    cmd = dict()
    cmd["type_"] = "set_s3_secret_access_key"
    cmd["name_"] = ""

    sock = comm.send_and_get_socket(cmd)

    comm.send_string(sock, value)

    msg = comm.recv_string(sock)

    if msg != "Success!":
        comm.engine_exception_handler(msg)


# --------------------------------------------------------------------------

__all__ = ("set_s3_access_key_id", "set_s3_secret_access_key")
