import struct
from functions.function_ids import functionId
import bitstring
import math
import string
import queue

class VcdGenerator:
    def __init__(self, timeScale):
        self.timeScale = timeScale
        self.chars = string.printable
        self.lastBits = None

    def getNextChar(self, c):
        p = self.chars.find(c)
        p += 1
        if p >= len(self.chars):
            p = 0
        return self.chars[p]

    def getNextShortname(self, sn):
        if sn is None:
            return self.chars[0]
        for i in range(len(sn)):
            ls = list(sn)
            ls[i]=self.getNextChar(sn[i])
            sn = ''.join(ls)
            if sn[i]!=self.chars[0]:
                break
        else:
            sn+=self.chars[0]
        return sn
            

    def getVariableNames(self, bitarr):
        variables = []
        sn = None
        for b in range(len(bitarr[0])):
            sn = self.getNextShortname(sn)
            variables.append(('bit%d'%(b), sn))
        return variables

    def genBits(self, bits, variableNames):
        o = ""
        for b in range(len(bits)):
            if self.lastBits is None:
                o+="%d"%(bits[b])+ variableNames[b][1]+"\n"
            else:
                if self.lastBits[b] != bits[b]:
                    o+="%d"%(bits[b])+ variableNames[b][1]+"\n"
        self.lastBits = bits
        return o  

    def getVcdString(self, bitarr):
        variableNames = self.getVariableNames(bitarr)
        out="$version the best vcd in the universe $end\n"
        out+="$timescale "+self.timeScale+" $end\n"
        out+="$scope module debug_core $end\n"
        for v in variableNames:
            out+="$var reg 1 "+v[1]+" "+v[0]+" $end\n"
        out+="$upscope $end\n"
        out+="$enddefinitions $end\n"
        out+="$dumpvars\n"
        for i in range(len(bitarr)):
            if i > 0:
                out+="#%d\n"%(i)
            out+=self.genBits(bitarr[i], variableNames)
        return out

class DebugCore:
    def __init__(self, addr, writer):
        self.q = queue.Queue()
        self.addr = addr
        self.writer = writer
        #print("Created Debug Core with address:", self.addr)
    
    def setup(self, frame):
        (fid, self.width, self.depth)=struct.unpack("III", frame[0:12])
        #print("frame", frame, fid, self.width, self.depth)
        if fid != functionId['debug_core']:
            raise ValueError("Invalid function id for debug core")
        print("Setup debugcore with bus width:", self.width, "fifo depth:", self.depth)

    def put(self, frame):
        self.q.put(frame)

    def dataStringToWordsPayload(self,data):
        wordSize = 1;
        maskBytes = math.ceil(self.width/(wordSize*8))
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

    def setReferenceWord(self, mask):
        header = struct.pack("III", 0x00000001, 0, 0)
        data = self.dataStringToWordsPayload(mask)
        #print(len(header+data),len(header), len(data), len(mask))
        frame = self.addr+header+data;
        self.writer.writeFrame(frame)
        
    def setCareMask(self, mask):
        header = struct.pack("III", 0x00000002, 0, 0)
        data = self.dataStringToWordsPayload(mask)
        frame = self.addr+header+data;
        self.writer.writeFrame(frame)
        
    def setArm(self):
        av = 1;
        header = struct.pack("III", 0x00000003, av, 0)
        data = self.dataStringToWordsPayload(self.width*'0')
        frame = self.addr+header+data;
        self.writer.writeFrame(frame)

    def receiveData(self):
        count = 0
        data = []
        while True:
            try:
                payload = self.q.get(timeout=1)
            except queue.Empty:
                print("Timeout after", len(data), "words")
                return data
            (fid, length, current) = struct.unpack("III", payload[0:12])
            tword = list(payload[12:])
            tword.reverse()
            tword = bytes(tword)
            data.append(bitstring.BitArray(reversed(list(bitstring.BitArray(tword)))))
            if length -1 == current:
                break
        return data

    def dumpVcd(self, fileName):
        dbdat = self.receiveData();
        print("Got", len(dbdat), "words of data")
        vg = VcdGenerator("1ps")
        f = open(fileName, 'w')
        f.write(vg.getVcdString(dbdat))
        f.close()
