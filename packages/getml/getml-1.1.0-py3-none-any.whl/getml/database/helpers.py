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
Collection of helper functions not meant to be used by the enduser.
"""

import io
from pathlib import Path
from urllib import request
from urllib.parse import urlparse

import getml.communication as comm

# -----------------------------------------------------------------------------


def _load_to_buffer(url):

    pb = comm._ProgressBar()

    with request.urlopen(url) as response:
        length = response.getheader("content-length")
        block_size = 8192

        if length:
            length = int(length)
            block_size = max(4096, length // 100)

        buffer = io.BytesIO()

        pb.show(0)

        finished = 0

        while True:
            block = response.read(block_size)
            if not block:
                break
            finished += len(block)
            buffer.write(block)
            percent = int((finished / length) * 100)
            pb.show(percent)

        print()

        return buffer


# --------------------------------------------------------------------


def _retrieve_temp_dir():
    cmd = {"name_": "", "type_": "temp_dir"}
    sock = comm.send_and_get_socket(cmd)
    temp_dir = comm.recv_string(sock)
    sock.close()
    return temp_dir


# --------------------------------------------------------------------


def _retrieve_url(url, verbose=True):
    parse_result = urlparse(url)

    target_path = Path(
        _retrieve_temp_dir() + "downloads/" + parse_result.netloc + parse_result.path
    ).expanduser()

    if target_path.exists():
        return target_path.as_posix()

    target_path.parent.mkdir(parents=True, exist_ok=True)

    with open(target_path, "wb") as file:
        if verbose:
            print(f"Downloading {target_path.name}...")
        buf = _load_to_buffer(url)
        file.write(buf.getbuffer())

    return target_path.as_posix()


# --------------------------------------------------------------------


def _retrieve_urls(fnames, verbose=True):
    def is_url(fname):
        return urlparse(fname).scheme != ""

    return [
        _retrieve_url(fname, verbose)
        if is_url(fname)
        else Path(fname).expanduser().absolute().as_posix()
        for fname in fnames
    ]
