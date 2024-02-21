import struct
from functions.function_ids import functionId
import bitstring
import math
import string
import queue

class MdioInterface:
    def __init__(self, addr, writer):
        self.q = queue.Queue()
        self.addr = addr
        self.writer = writer
    
    def put(self, frame):
        self.q.put(frame)

    def readRegister(self, phyAddr, regAddr):
        word = 1+(phyAddr<<1)+(regAddr<<6)
        payload = struct.pack("I", word)
        with self.q.mutex:
            self.q.queue.clear()
        self.writer.writeFrame(self.addr+bytes(payload))
        responsePayload = self.q.get()
        d = struct.unpack("I", responsePayload)
        return  d[0]>>16

    def writeRegister(self, phyAddr, regAddr, regValue):
        word = 0+(phyAddr<<1)+(regAddr<<6) +(regValue<<16)
        payload = struct.pack("I", word)
        self.writer.writeFrame(self.addr+bytes(payload))
        a = self.q.get()
