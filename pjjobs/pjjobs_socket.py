# This file is part of PJJobs project.
# The COPYRIGHT file at the top level of this repository
# contains the full copyright notices and license terms.

import json
import socket


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
            header = str(len(msg))
            self._send(header)
            self._send(msg)

    def read_obj(self):
        size = self._msg_length()
        data = self._read(size)
        return json.loads(data)

    def _send(self, msg):
        msg = msg.encode('utf-8')
        sent = 0
        while sent < len(msg):
            sent += self.socket.send(msg[sent:])

    def _read(self, size):
        data = ''
        while len(data) < size:
            data_tmp = self.socket.recv(size - len(data))
            data += data_tmp.decode('utf-8')
            if data_tmp == '':
                raise RuntimeError("socket connection broken")
        return data

    def _msg_length(self):
        d = self._read(2) #TODO should be len(MAX_MESSAGE_SIZE)
        return int(d)

    def close(self):
        self.socket.close()

    def _get_timeout(self):
        return self._timeout

    def _set_timeout(self, timeout):
        self._timeout = timeout
        self.socket.settimeout(timeout)
