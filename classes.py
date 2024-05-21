#!./venv/bin/python

import socket, pickle, json

class empty_class:
    pass

class notificationCore:
    def __init__(self):
        self.notificationCore = None
        self.user_id = None
        self.pv = None
        self.limit = None
        self.limitLL = None
        self.limitLU = None
        self.rule = None
        self.subrule = None

class notification_id:
    def __init__(self):
        self.notification_id = None
        self.notificationCore = notificationCore()

class NotificationInfoByPV2:
    def __init__(self):
        self.notification_id = notification_id()
    def notification_number(self):
        return len(self.notificationCore)

class NotificationInfoByPV:
    def __init__(self):
        self.notification_id = None
        self.notificationCore = None
        self.user_id = None
        self.pv = None
        self.limit = None
        self.limitLL = None
        self.limitLU = None
        self.rule = None
        self.subrule = None
    def notification_number(self):
        return (self.notificationCore)


class socketClient:
    def __init__(self, address, debug=False):
        self.address = address
        self.debug = debug

    def create_socket(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            return sock
        except Exception as e:
            return 'error on create_socket', e

    def connect(self, sock):
        try:
            sock.connect(self.address)
            return 'ok'
        except Exception as e:
            return e

    def send_data(self, sock, data):
        try:
            sock.sendall(pickle.dumps(data))
            return 'ok'
        except Exception as e:
            return 'error on send_data', e

    def receive_data(self, sock, size, echo=False):
        try:
            data = sock.recv(size)
            if echo:
                sock.sendall(data) # echo
            return pickle.loads(data)
        except Exception as e:
            return 'error on receive_data', e

    def close(self, sock):
        sock.close()
