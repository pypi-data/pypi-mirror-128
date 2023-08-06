from omnitools import FTPESS, FTPS
import threading
import time
import os


class FTPRelayFO:
    def __init__(self):
        self.buffer = []
        self.name = None
        self.closed = False
        self.timeout = 5
        self.parts = 0
        self.length = 0

    def read(self, n: int):
        tried = 0
        while True:
            try:
                r = None
                try:
                    r = self.buffer.pop(0)
                    return r
                except:
                    raise
                finally:
                    pass
            except IndexError:
                if self.closed:
                    return b""
                if tried < self.timeout:
                    tried += 1
                    time.sleep(1)

    def write(self, s: bytes):
        self.buffer.append(s)
        self.parts += 1
        _ = len(s)
        self.length += _
        return _

    def fileno(self):
        raise AttributeError("do not use sendfile()")

    def close(self):
        self.closed = True

    def flush(self):
        pass


def fake_remote_server_setup(server_type, credentials):
    if not credentials:
        credentials = ["foxe6"]*2
    port = 8022
    users = credentials+["elradfmwMT"]
    remote_homebase = os.path.abspath(r"s2")
    s2 = server_type(port=port)
    s2.server.max_cons = 10
    s2.server.max_cons_per_ip = 10
    homedir = os.path.join(remote_homebase, users[0])
    os.makedirs(homedir, exist_ok=True)
    s2.handler.authorizer.add_user(*users[:2], homedir, users[-1])
    if issubclass(server_type, FTPESS):
        s2.handler.certfile = os.path.join(remote_homebase, "foxe2.pem")
        s2.handler.tls_control_required = True
        s2.handler.tls_data_required = True
    s2.handler.passive_ports = range(51200, 52200)
    s2.configure()
    p2 = threading.Thread(target=s2.start)
    p2.daemon = True
    p2.start()
    return ["127.0.0.1", port], credentials


def fake_ftpes_remote_server_setup(credentials: list = None):
    return fake_remote_server_setup(FTPESS, credentials)


def fake_ftps_remote_server_setup(credentials: list = None):
    return fake_remote_server_setup(FTPS, credentials)


