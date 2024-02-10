from tcp import TcpClient
import socket
import time
import function_ids
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

class Escaper:
    def __init__(self, esc, end):
        self.esc = esc
        self.end = end

    def escaped(self, data):
        if data == self.esc:
            return [self.esc, data]
        return [data]

    def generateFrame(self, data):
        output = []
        for d in data[0:-1]:
            output+= self.escaped(d)
        output+=[self.esc, self.end]
        output+=self.escaped(data[-1])
        return bytes(output)

class FpgaInterface:
    def __init__(self, cli):
        self.deescaper = DeEscaper(0xc0, 0x03)
        self.escaper = Escaper(0xc0, 0x03)
        self.cli = cli
        self.addressMap = {}

    def getFrame(self):
        while True:
            d = self.cli.recv(1)
            if d is not None and len(d) > 0:
                self.deescaper.addData(d)
                frame = self.deescaper.getFrame()
                if frame is not None:
                    return bytes(frame)

    def sendFrame(self, data):
        self.cli.send(self.escaper.generateFrame(data))

    def getDiscoveryFrames(self):
        self.sendFrame([0xff])
        frames = {}
        rxFrames = 0
        while True:
            frame = self.getFrame()
            rxFrames+=1
            if frame in frames:
                frames[frame]+=1
            else:
                frames[frame]=1
            if rxFrames == 2:
                self.sendFrame([0xFF])
            if rxFrames > 4:
                complete=True
                for frame in frames:
                    if frames[frame] != 2:
                        complete = False
                if complete:
                    break;
        return frames

    def lookupFunction(self, fid):
        for funcName in function_ids.functionId:
            if function_ids.functionId[funcName] == fid:
                return funcName

    def lookupAddress(self, frame):
            for addr in self.addressMap:
                if addr == frame[0:len(addr)]:
                    return self.addressMap[addr]

    def initialize(self):
        frames = self.getDiscoveryFrames()
        for frame in frames:
            if frame[-1] == 0xFF:
                print("Loopback frame", frame)
            
            if self.lookupAddress(frame) is None:
                funcName = self.lookupFunction(frame[-1])
                if funcName is not None:
                    self.addressMap[frame[0:-1]]=funcName
                    print("Frame", frame, "is ident for:", funcName)
            else:
                print("Frame", frame, "is extra information for:", self.lookupAddress(frame))

print("Creating client")
cli = TcpClient("localhost", 8080)
cli.sck.settimeout(0.1)
iface = FpgaInterface(cli)
iface.initialize()
