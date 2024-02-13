from tcp import TcpClient
import socket
import time
import functions.functions
import struct

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

class DebugCore:
    def __init__(self):
        pass
    
    def setup(self, frame):
        pass
        

class FpgaInterface:
    def __init__(self, cli):
        self.bc = 0xff
        self.deescaper = DeEscaper(0xc0, 0x03)
        self.escaper = Escaper(0xc0, 0x03)
        self.cli = cli
        self.functionMap = {}

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
        self.sendFrame([self.bc])
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
                self.sendFrame([self.bc])
            if rxFrames > 4:
                complete=True
                for frame in frames:
                    if frames[frame] != 2:
                        complete = False
                if complete:
                    break;
        return frames

    def getAddressAndPayload(self, frame):
        addr = []
        nAddrBytes = 0
        for b in frame:
            if b==self.bc:
                break
            addr.append(b)
            nAddrBytes+=1
        payload = frame[nAddrBytes+1:]
        return bytes(addr), bytes(payload)

    def initialize(self):
        frames = self.getDiscoveryFrames()
        for frame in frames:
            addr, payload = self.getAddressAndPayload(frame)

            if len(addr) == 0:
                print("Loopback frame", frame)
            else:
                if addr not in self.functionMap:
                    self.functionMap[addr] = functions.functions.functionMap[int.from_bytes(payload)](addr, self)
                else:
                    self.functionMap[addr].setup(payload)

print("Creating client")
cli = TcpClient("localhost", 8080)
cli.sck.settimeout(0.2)
iface = FpgaInterface(cli)
iface.initialize()
dbg = iface.functionMap[b'\x01']
dbg.setAndMask('1'*73)
dbg.setOrMask('1'*73)
dbg.setArm()
dbg.receiveData()

dbg2 = iface.functionMap[b'\x03']
dbg2.setAndMask('1'*13)
dbg2.setOrMask('1'*13)
dbg2.setArm()
print(dbg2.receiveData())


dbg.setArm()
dbg.receiveData()
time.sleep(0.1)
