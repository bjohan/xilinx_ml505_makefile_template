import socket
import select 
import errno

class TcpServerClient:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr

    def recv(self, n=1024):
        return self.conn.recv(n)

    def send(self, d):
        return self.conn.send(d)

    def connectionValid(self):
        try:
            b = self.conn.recv(1, socket.MSG_PEEK | socket.MSG_DONTWAIT)
            if b == b'':
                return False
        except BlockingIOError as e:
            if e.errno != errno.EAGAIN:
                raise
        return True

class TcpServer:
    def __init__(self, host, port):
        self.sck = socket.socket()
        self.sck.bind((host, port))
        self.sck.listen(2)

    def getConnection(self):
        conn, addr = self.sck.accept()
        return TcpServerClient(conn, addr)

class TcpClient:
    def __init__(self, host, port):
        self.sck = socket.socket()
        self.sck.connect((host, port))
    
    def recv(self, n=1024):
        return self.sck.recv(n)

    def send(self, d):
        return self.sck.send(d)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        print("S: Creating server")
        srv = TcpServer(sys.argv[1], int(sys.argv[2]))
        print("S: Server started, waiting for connection")
        conn = srv.getConnection()
        print("S: Got connection, waiting for message")
        msg = conn.recv();
        print("S: Got", msg)
        conn.send(msg)
        print("S: Sent back", msg)
    elif len(sys.argv) == 4:
        print("C: Creating client")
        cli = TcpClient(sys.argv[1], int(sys.argv[2]))
        print("C: Client created, sending message:", sys.argv[3])
        cli.send(bytes(sys.argv[3], "ascii"))
        print("C: Waiting for response")
        resp = cli.recv();
        print("C: Got response:", resp)
        for i in range(len(sys.argv[3])-2): 
            print(cli.recv())
    else:
        print("Usage:")
        print("For server:", sys.argv[0], "host port") 
        print("For client:", sys.argv[0], "host port message") 
    
