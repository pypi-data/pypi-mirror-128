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
Reads a list of CSV files located in an S3 bucket.
"""


import getml.communication as comm

from .connection import Connection


def read_s3(
    name,
    bucket,
    keys,
    region,
    sep=",",
    num_lines_read=0,
    skip=0,
    colnames=None,
    conn=None,
):
    """
    Reads a list of CSV files located in an S3 bucket.

    Example:
        Let's assume you have two CSV files - *file1.csv* and
        *file2.csv* - in the bucket. You can
        import their data into the getML engine using the following
        commands:

        >>> getml.engine.set_s3_access_key_id("YOUR-ACCESS-KEY-ID")
        >>>
        >>> getml.engine.set_s3_secret_access_key("YOUR-SECRET-ACCESS-KEY")
        >>>
        >>> stmt = data.database.sniff_s3(
        ...         bucket="your-bucket-name",
        ...         keys=["file1.csv", "file2.csv"],
        ...         region="us-east-2",
        ...         name="MY_TABLE",
        ...         sep=';'
        ... )
        >>>
        >>> getml.database.execute(stmt)
        >>>
        >>> stmt = data.database.read_s3(
        ...         bucket="your-bucket-name",
        ...         keys=["file1.csv", "file2.csv"],
        ...         region="us-east-2",
        ...         name="MY_TABLE",
        ...         sep=';'
        ... )

        You can also set the access credential as environment variables
        before you launch the getML engine.

    Args:
        name (str):
            Name of the table in which the data is to be inserted.

        bucket (str):
            The bucket from which to read the files.

        keys (List[str]):
            The list of keys (files in the bucket) to be read.

        region (str):
            The region in which the bucket is located.

        sep (str, optional):
            The separator used for separating fields. Default:`,`

        num_lines_read (int, optional):
            Number of lines read from each file.
            Set to 0 to read in the entire file.

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
    """
    # -------------------------------------------

    conn = conn or Connection()

    # -------------------------------------------
    # Prepare command.

    cmd = dict()

    cmd["name_"] = name
    cmd["type_"] = "Database.read_s3"

    cmd["bucket_"] = bucket
    cmd["keys_"] = keys
    cmd["num_lines_read_"] = num_lines_read
    cmd["region_"] = region
    cmd["sep_"] = sep
    cmd["skip_"] = skip
    cmd["conn_id_"] = conn.conn_id

    if colnames is not None:
        cmd["colnames_"] = colnames

    # -------------------------------------------
    # Send JSON command to engine.

    comm.send(cmd)
