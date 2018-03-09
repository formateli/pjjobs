# This file is part of PJJobs project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import json
import socket
import struct


class JsonSocket(object):
    def __init__(self, address='127.0.0.1', port=9090, use_socket=None):
        if use_socket is None:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = use_socket
        self._timeout = None
        self._address = address
        self._port = port

    def send_obj(self, obj):
        msg = json.dumps(obj)
        if self.socket:
            frmt = "=%ds" % len(msg)
            packed_msg = struct.pack(frmt, msg)
            packed_hdr = struct.pack('!I', len(packed_msg))

            self._send(packed_hdr)
            self._send(packed_msg)
			
    def _send(self, msg):
        sent = 0
        while sent < len(msg):
            sent += self.socket.send(msg[sent:])

    def _read(self, size):
        data = ''
        while len(data) < size:
            data_tmp = self.socket.recv(size-len(data))
            data += data_tmp
            if data_tmp == '':
                raise RuntimeError("socket connection broken")
        return data

    def _msg_length(self):
        d = self._read(4)
        s = struct.unpack('!I', d)
        return s[0]

    def read_obj(self):
        size = self._msg_length()
        data = self._read(size)
        frmt = "=%ds" % size
        msg = struct.unpack(frmt, data)
        return json.loads(msg[0])

    def close(self):
        self.socket.close()

    def _get_timeout(self):
        return self._timeout

    def _set_timeout(self, timeout):
        self._timeout = timeout
        self.socket.settimeout(timeout)
