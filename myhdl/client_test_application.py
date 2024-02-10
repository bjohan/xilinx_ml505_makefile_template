from tcp import TcpClient
import socket
import time
class DeEscaper:
    def __init__(self, esc, end):
        self.esc = esc;
        self.end = end;
        self.data = []
        
    def addData(self, d):
        self.data+=d

    def getFrame(self):
        escaped = False
        nextIsLast = False
        payload = []
        consumed = 0
        for d in self.data:
            consumed+=1
            if escaped:
                if d == self.esc:
                    payload.append(d)
                    if nextIsLast:
                        self.data = self.data[consumed:]
                        return payload
                elif d == self.end:
                    nextIsLast = True
                else:
                    raise ValueError("Corrpupt stream, only escape and end shall be escaped")
                escaped = False
            elif d == self.esc:
                escaped=True
            else:
                escaped=False
                payload.append(d)
                if nextIsLast:
                    self.data = self.data[consumed:]
                    return payload
        return None

print("Creating client")
cli = TcpClient("localhost", 8080)
cli.sck.settimeout(0.1)
print("Connected to testbench")
t0=time.time()
cli.send(bytes([0xC0]))
cli.send(bytes([0x03]))
cli.send(bytes([0xFF]))
time.sleep(0.05)
cli.send(bytes([0xC0]))
cli.send(bytes([0x03]))
cli.send(bytes([0xFF]))
de = DeEscaper(0xc0, 0x03)
print("Waiting for response from tb")
frameCounts = {}
while True:
    try:
        d = cli.recv(1)
        if d is not None and len(d) > 0:
            #print("Got", d, "at", time.time()-t0)
            de.addData(d)
            frame = de.getFrame()
            if frame is not None:
                frame=bytes(frame)
                print("Got frame:", bytes(frame))
                if frame in frameCounts:
                    frameCounts[frame] +=1
                else:
                    frameCounts[frame] =1
            if len(frameCounts.keys()):
                complete=True
                for frame in frameCounts.keys():
                    if frameCounts[frame] != 2:
                        complete = False
                if complete:
                    print("Init complete")
                    break
    except TimeoutError:
        break
print("Duration", time.time()-t0)
