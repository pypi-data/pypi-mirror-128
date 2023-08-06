import asyncore
import sys
import socket
import time
from typing import NamedTuple, Callable, Any
from enum import Enum

class SocketType(Enum):
    TCP_CLIENT = 'tcp_client'
    TCP_SERVER = 'tcp_server'
    UDP_CLIENT = 'udp_client'
    UDP_SERVER = 'udp_server'

class SocketConfig(NamedTuple):
    MODE: SocketType
    HOST: str
    PORT: int
    POOL: int = 0
    BUFFER: int = 1024
    LISTEN: int = 500
    TIME_OUT: int = 5
    CALL_BACK: dict = {}
    HANDLE_CLASS: Any = None
    PARAENT_CLASS: Any = None

class SocketClient(asyncore.dispatcher):

    def __init__(self, config: SocketConfig):
        asyncore.dispatcher.__init__(self)
        self.config = config
        if self.config.MODE == SocketType.TCP_CLIENT:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.connect((self.config.HOST, self.config.PORT))

    def handle_connect(self):
        pass

    def writable(self):
        return True

    def handle_write(self):
        pass

    def readable(self):
        return False

    def handle_read(self):
        data = self.recv(self.config.BUFFER)
        if len(data) > 0 and self.config.CALL_BACK is not None:
            self.config.CALL_BACK(data)

    def handle_error(self):
        t, e, trace = sys.exc_info()
        print(e)
        self.close()

    def handle_close(self):
        self.close()

class SocketHandler(asyncore.dispatcher_with_send):

    def __init__(self, config: SocketConfig, sock=None, addr=None):
        asyncore.dispatcher_with_send.__init__(self, sock)
        self.config = config
        self.addr = addr

    def handle_read(self):
        data = self.recv(self.config.BUFFER)
        
    def handle_close(self):
        super(SocketHandler, self).handle_close()

class SocketServer(asyncore.dispatcher):

    def __init__(self, config: SocketConfig):
        asyncore.dispatcher.__init__(self)
        self.config = config
        if self.config.MODE == SocketType.TCP_SERVER:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.create_socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.set_reuse_addr()
        self.bind((self.config.HOST, self.config.PORT))

        if self.config.MODE == SocketType.TCP_SERVER:
            self.listen(self.config.LISTEN)

    def handle_accept(self):
        client = self.accept()
        if client is not None:
            sock, addr = client
            if self.verify_request(sock, addr) is True:
                if self.config.HANDLE_CLASS is not None:
                    self.config.HANDLE_CLASS(self.config, sock, addr, self)

    def verify_request(self, sock, address):
        return True

class SocketAccessor:

    def __init__(self, config: SocketConfig):
        self.config = config

    def loop(self):
        if self.config.MODE in [SocketType.TCP_SERVER, SocketType.UDP_SERVER]:
            SocketServer(self.config)
        else:
            SocketClient(self.config)

        if self.config.POOL == 0:
            asyncore.loop()
        else:
            while True:
                asyncore.loop(timeout=self.config.TIME_OUT)
                time.sleep(self.config.POOL)


