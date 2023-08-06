from robertcommon.system.io.socket import SocketType, SocketConfig, SocketAccessor

def call_back(data):
    print(data)

def test_tcp_client():
    config = SocketConfig(MODE=SocketType.UDP_SERVER, HOST='0.0.0.0', PORT=1000, CALL_BACK=call_back)
    accessor = SocketAccessor(config)
    accessor.loop()

test_tcp_client()