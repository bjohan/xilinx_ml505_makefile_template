import struct
from functions.function_ids import functionId
import bitstring

class DebugCore:
    def __init__(self, addr, iface):
        self.addr = addr
        self.iface = iface
        print("Created Debug Core with address:", self.addr)
    
    def setup(self, frame):
        (fid, self.width, self.depth)=struct.unpack("III", frame[0:12])
        if fid != functionId['debug_core']:
            raise ValueError("Invalid function id for debug core")
        print("Setup debugcore with bus width:", self.width, "fifo depth:", self.depth)
        
    def dataStringToWordsPayload(self,data):
        wordSize = 1;
        maskBytes = int(self.width/(wordSize*8)+1)
        payload = []
        for b in range(maskBytes):
            s = b*wordSize*8
            e = (b+1)*wordSize*8
            if e > len(data):
                e= len(data)
            asInt = int(data[s:e],2)
            d = struct.pack('B', asInt)
            payload.append(d[0])
        return bytes(payload)

    def setAndMask(self, mask):
        header = struct.pack("III", 0x00000001, 0, 0)
        data = self.dataStringToWordsPayload(mask)
        frame = self.addr+header+data;
        self.iface.sendFrame(frame)
        
    def setOrMask(self, mask):
        header = struct.pack("III", 0x00000002, 0, 0)
        data = self.dataStringToWordsPayload(mask)
        frame = self.addr+header+data;
        self.iface.sendFrame(frame)
        
    def setArm(self, trigOnAnd=True, trigOnOr=True):
        av = 0;
        if trigOnAnd:
            av+=1
        if trigOnOr:
            av+=2
        header = struct.pack("III", 0x00000003, av, 0)
        data = self.dataStringToWordsPayload(self.width*'0')
        frame = self.addr+header+data;
        self.iface.sendFrame(frame)

    def receiveData(self):
        count = 0
        while True:
            frame = self.iface.getFrame()
            addr, payload = self.iface.getAddressAndPayload(frame)
            (fid, length, current) = struct.unpack("III", payload[0:12])
            tword = list(payload[12:])
            tword.reverse()
            tword = bytes(tword)
            print(fid, length, current, bitstring.BitArray(tword))
            if length -1 == current:
                break
