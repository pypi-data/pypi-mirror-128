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
A handle to a database connection on the getML engine.
"""

import json

import getml.communication as comm
from getml.utilities.formatting import _SignatureFormatter


class Connection:
    """
    A handle to a database connection on the getML engine.

    Args:
        conn_id (str, optional):
            The name you want to use to reference the connection.
            You can call it
            anything you want to. If a database
            connection with the same conn_id already exists, that connection
            will be removed automatically and the new connection will take its place.
            The default conn_id is "default", which refers to the default connection.
            If you do not explicitly pass a connection handle to any function that
            relates to a database, the default connection will be used automatically.
    """

    def __init__(self, conn_id="default"):
        self.conn_id = conn_id

    def __repr__(self):
        return str(self)

    def __str__(self):

        cmd = dict()

        cmd["name_"] = self.conn_id
        cmd["type_"] = "Database.describe_connection"

        sock = comm.send_and_get_socket(cmd)

        msg = comm.recv_string(sock)

        if msg != "Success!":
            comm.engine_exception_handler(msg)

        description = comm.recv_string(sock)

        sock.close()

        json_obj = json.loads(description)

        json_obj["type"] = "Connection"

        sig = _SignatureFormatter(data=json_obj)

        return sig._format()
