import struct
from functions.function_ids import functionId
import bitstring
import math
import string
import queue

class BitField:
    def __init__(self, name, bits, value=0):
        self.name = name
        self.bits = bits

    def getBit(self, value, bit):
        return (value >> bit)&1

    def getBits(self, value):
        values = []
        for bit in self.bits:
            values.append(self.getBit(value, bit))
        return values

class Register:
    def __init__(self, name, fields, value=None):
        self.name = name
        self.fields = fields
        self.value = value

    def assign(self, value):
        self.value = value
        return self

    def __str__(self):
        o = self.name+'\n'
        for f in self.fields:
            o+='\t'+f.name+' '+str(f.getBits(self.value))+'\n'
        return o

reg0 = Register('control register', [
        BitField("Reset", [15]),
        BitField("Loopback", [14]),
        BitField("Speed sel lsb", [13]),
        BitField("aneg enable", [12]),
        BitField("power down", [11]),
        BitField("isolate", [10]),
        BitField("restart aneg", [9]),
        BitField("cu duplex mode", [8]),
        BitField("collision test", [7]),
        BitField("speed selection msb", [6]),
        BitField("reserved", range(6))])

reg1 = Register('status register', [
        BitField("100base-t4", [15]),
        BitField("100base-x full duplex", [14]),
        BitField("100base-x half duplex", [13]),
        BitField("10 mbps full duplex", [12]),
        BitField("10 mbps half duplex", [11]),
        BitField("100base t2 full duplex", [10]),
        BitField("100base t2 half duplex", [9]),
        BitField("extended status", [8]),
        BitField("reserved", [7]),
        BitField("mf preamble suppression", [6]),
        BitField("cu aneg compatible", [5]),
        BitField("cu remote fault", [4]),
        BitField("auto aneg ability", [3]),
        BitField("cu link status", [2]),
        BitField("jabber detect", [1]),
        BitField("exteded capability", [9]),
])

reg2 = Register("phy identifier 0", [
        BitField("OUI 3:18", range(16))
])

reg3 = Register("phy identifier 1", [
        BitField("OUI 3:18", [10, 11, 12, 13, 14, 15]),
        BitField("Model", [4, 5, 6, 7, 8, 9]),
        BitField("Rev", [0,1,2,3]),
])

reg4 = Register("aneg advertise", [
        BitField("next page", [15]),
        BitField("ack", [14]),
        BitField("remote fault", [13]),
        BitField("reserved", [12]),
        BitField("asymmetric pause", [11]),
        BitField("pause", [10]),
        BitField("100base t4", [9]),
        BitField("100base tx full duplex", [8]),
        BitField("100base-tx half duplex", [7]),
        BitField("10base-tx full duplex", [6]),
        BitField("10base-tx half duplex", [5]),
        BitField("sector field", range(5)),
])

reg5 = Register("link layer ability", [
        BitField("next page", [15]),
        BitField("ack", [14]),
        BitField("remote fault", [13]),
        BitField("technology ability", [12]),
        BitField("asymetric pause", [11]),
        BitField("pause capable", [10]),
        BitField("100base t4 capability", [9]),
        BitField("100basetx full duplex capability", [8]),
        BitField("100basetx half duplex capability", [7]),
        BitField("10base-t full duplex capability", [6]),
        BitField("10base-t half duplex capability", [5]),
        BitField("sector field", range(5)),
])

reg6 = Register("aneg expansion", [
        BitField("Reserved", range(5,16)),
        BitField("parallell detectio fault", [4]),
        BitField("link partner next page able", [3]),
        BitField("local next page able", [2]),
        BitField("page received", [1]),
        BitField("link partner autoneg", [0]),
])

reg7 = Register("next page transmit", [
        BitField("next page", [15]),
        BitField("reserved", [14]),
        BitField("message page mode", [13]),
        BitField("acknowledge", [12]),
        BitField("toggle", [11]),
        BitField("message/unformatted field", range(11)),
])

reg8 = Register("link partner next page", [
        BitField("next page", [15]),
        BitField("ack", [14]),
        BitField("message page", [13]),
        BitField("ack2", [12]),
        BitField("toggle", [11]),
        BitField("message/unformatted field", range(11)),
])

reg9 = Register("1000base-t control", [
        BitField("test mod", [13, 14, 15]),
        BitField("master/slave manual config enable", [12]),
        BitField("master/slave configuration variable", [11]),
        BitField("port type", [10]),
        BitField("1000base-t full duplex", [9]),
        BitField("1000base-t half duplex", [8]),
        BitField("reserved", range(8)),
])


reg10 = Register("1000base-t status", [
        BitField("master/slave config fault", [15]),
        BitField("master/slave config resolution", [14]),
        BitField("local receiver status", [13]),
        BitField("remote receiver status", [12]),
        BitField("link partner 1000base-t full duplex capability", [11]),
        BitField("link partner 1000base-t half duplex capability", [10]),
        BitField("reserved", [8,9]),
        BitField("idle error count",range(8)),
])

reg11 = Register("reserved", [BitField("reserved", range(16))])
reg12 = Register("reserved", [BitField("reserved", range(16))])
reg13 = Register("reserved", [BitField("reserved", range(16))])
reg14 = Register("reserved", [BitField("reserved", range(16))])

reg15 = Register("extended status", [
        BitField("1000base-x full duplex", [15]),
        BitField("1000base-x half duplex", [14]),
        BitField("1000base-t full duplex", [13]),
        BitField("1000base-t half duplex", [12]),
        BitField("reserved", range(12)),
])

reg16 = Register("phy specific control", [
        BitField("transmit fifo depth", [14,15]),
        BitField("receive fifo depth", [12, 13]),
        BitField("assert crs on transmit", [11]),
        BitField("force link good", [10]),
        BitField("energy detect", [8, 9]),
        BitField("enable extended distance", [7]),
        BitField("MDI crossover mode", [5,6]),
        BitField("disable 125clk", [4]),
        BitField("mac interface power down", [3]),
        BitField("sqe test", [2]),
        BitField("polarity reversal", [1]),
        BitField("disable jabber", [0]),
])

reg17 = Register("phy specific status copper", [
        BitField("speed", [14, 15]),
        BitField("duplex", [13]),
        BitField("page received", [12]),
        BitField("speed and duplex resolved", [11]),
        BitField("link (real time)", [10]),
        BitField("cable length(1000 mode only)", [7, 8, 9]),
        BitField("mdi crossover status", [6]),
        BitField("downshift status", [5]),
        BitField("copper energy detect status", [4]),
        BitField("transmit pause enabled", [3]),
        BitField("receive pause enabled", [2]),
        BitField("polarity (real time)", [1]),
        BitField("jabber (real time)", [0]),
])

reg18 = Register("interrupt enable", [
        BitField("aneg error", [15]),
        BitField("speed changed", [14]),
        BitField("duplex change", [13]),
        BitField("page received", [12]),
        BitField("aneg complete", [11]),
        BitField("link status change", [10]),
        BitField("symbol error", [9]),
        BitField("false carrier", [8]),
        BitField("fifo overflow/underflow", [7]),
        BitField("mdi corssover change", [6]),
        BitField("downshift", [5]),
        BitField("energy detect", [4]),
        BitField("reserved", [3]),
        BitField("dte power detection status change", [2]),
        BitField("polarity changed", [1]),
        BitField("jabber", [0]),
])

reg19 = Register("interrupt status", [
        BitField("aneg error", [15]),
        BitField("speed changed", [14]),
        BitField("duplex change", [13]),
        BitField("page received", [12]),
        BitField("aneg complete", [11]),
        BitField("link status change", [10]),
        BitField("symbol error", [9]),
        BitField("false carrier", [8]),
        BitField("fifo overflow/underflow", [7]),
        BitField("mdi corssover change", [6]),
        BitField("downshift", [5]),
        BitField("energy detect", [4]),
        BitField("reserved", [3]),
        BitField("dte power detection status change", [2]),
        BitField("polarity changed", [1]),
        BitField("jabber", [0]),
])


reg20 = Register("extended phy specific control", [
        BitField("block carrier extension", [15]),
        BitField("line loopback", [14]),
        BitField("reserved", [13]),
        BitField("disable lnk pulses", [12]),
        BitField("downshift counter", [9, 10, 11]),
        BitField("downshift enable", [8]),
        BitField("rgmii receive timing control", [7]),
        BitField("default mac interface speed", [4,5,6]),
        BitField("reserved", [3]),
        BitField("dte detect enable", [2]),
        BitField("rgmi transmit timing control", [1]),
        BitField("reserved", [0]),
])

reg21 = Register("receive error counter", [
        BitField("receive error count", range(16)),
])

reg22 = Register("extended address", [
        BitField("reserved", range(8,16)),
        BitField("page select for registers 0 to 28", range(8))
])

reg24 = Register("LED control", [
        BitField("disable led", [15]),
        BitField("pulse stretch duration", [12,13,14]),
        BitField("force interrupt", [11]),
        BitField("blink rate", [8, 9, 10]),
        BitField("led duplex control", [7]),
        BitField("led tx control", [6]),
        BitField("led link control", [3, 4, 5]),
        BitField("led duplex control", [2]),
        BitField("led rx control", [1]),
        BitField("led tx control", [0]),
])

reg25 = Register("manual led ovverride", [
        BitField("sgmii aneg timer", [14, 15]),
        BitField("reserved", [12, 13]),
        BitField("led duplex", [10, 11]),
        BitField("led link 10", [8, 9]),
        BitField("led link 100", [6, 7]),
        BitField("led link 1000", [4, 5]),
        BitField("led rx", [2, 3]),
        BitField("led tx", [0, 1]),
])

reg26 = Register("extended phy specific control", [
        BitField("reserved", [15]),
        BitField("fct pll loop bw control", [14]),
        BitField("fct xmit pre emphasis control", [13]),
        BitField("reserved ", [12]),
        BitField("autoselcet preferred media", [10, 11]),
        BitField("serdes pattern generation", [8, 9]),
        BitField("enable externa fiber signald detect input", [7]),
        BitField("fiber input impedance", [6]),
        BitField("fiber output impedance", [5]),
        BitField("fiber mode clock enable", [4]),
        BitField("reserved ", [3]),
        BitField("fiber output amplitude", [0,1,2]),
])

reg27 = Register("extended phy specific status", [
        BitField("Fiber/Copper auto selection disable", [15]),
        BitField("reserved", [14]),
        BitField("fiber/copper resolution", [13]),
        BitField("serial interface aneg bypass enable", [12]),
        BitField("serial interface aneg bypass status", [11]),
        BitField("interrupt polarity", [10]),
        BitField("disable/enable automatic medium register selection", [9]),
        BitField("dte detect status drop hysteresis", [5,6,7,8]),
        BitField("dte power status", [4]),
        BitField("hwconfig mode", range(4)),
])

reg28 = Register("virtual cable tester", [
        BitField("run vct test", [15]),
        BitField("status", [13, 14]),
        BitField("amplitude", [8,9,10,11,12]),
        BitField("distance", range(8)),
])


reg31 = Register("reserved", [BitField("reserved", range(16))])
#reg2 = Register("", [
#        BitField("", []),
#])

class MdioInterface:
    def __init__(self, addr, writer):
        self.q = queue.Queue()
        self.addr = addr
        self.writer = writer
        self.phyAddr = 7

    def setPhyAddr(self, phyAddr):
        self.phyAddr = phyAddr
    
    def put(self, frame):
        self.q.put(frame)

    def readRegister(self, regAddr):
        word = 1+(self.phyAddr<<1)+(regAddr<<6)
        payload = struct.pack("I", word)
        with self.q.mutex:
            self.q.queue.clear()
        self.writer.writeFrame(self.addr+bytes(payload))
        responsePayload = self.q.get()
        d = struct.unpack("I", responsePayload)
        return  d[0]>>16

    def writeRegister(self, regAddr, regValue):
        word = 0+(self.phyAddr<<1)+(regAddr<<6) +(regValue<<16)
        payload = struct.pack("I", word)
        self.writer.writeFrame(self.addr+bytes(payload))
        a = self.q.get()

    def assignBits(self, register, bits, bitPositions):
        a = readRegister(reg)
        for pos, bit in zip(bitPosition, bits):
            if bit:
                a = a | 1 << pos
            else:
                a = a & ~(1<< pos)
        a = a & 0xFFFFFF
        self.writeRegister(register, bits)

    def setBit(self,register, bit):
        a = self.readRegister(register)
        a = a | 1 << bit;
        self.writeRegister(register, a)

    def getBit(self, register, bit):
        a = self.readRegister(register)  
        return (a >> bit) | 1

    
    def printConfig(self):
        reg0.assign(self.readRegister(0))
        print(reg0)
        
        reg1.assign(self.readRegister(1))
        print(reg1)

        oui = self.readRegister(2)<<3+ ((self.readRegister(3)>>10)&0x3F)<<19
        print('OUI {:02x}'.format(oui))
        print(reg2.assign(self.readRegister(2)))
        print(reg3.assign(self.readRegister(3)))
        print(reg4.assign(self.readRegister(4)))
        print(reg5.assign(self.readRegister(5)))
        print(reg6.assign(self.readRegister(6)))
        print(reg7.assign(self.readRegister(7)))
        print(reg8.assign(self.readRegister(8)))
        print(reg9.assign(self.readRegister(9)))
        print(reg10.assign(self.readRegister(10)))
        print(reg11.assign(self.readRegister(11)))
        print(reg12.assign(self.readRegister(12)))
        print(reg13.assign(self.readRegister(13)))
        print(reg14.assign(self.readRegister(14)))
        print(reg15.assign(self.readRegister(15)))
        print(reg16.assign(self.readRegister(16)))
        print(reg17.assign(self.readRegister(17)))
        print(reg18.assign(self.readRegister(18)))
        print(reg19.assign(self.readRegister(19)))
        print(reg20.assign(self.readRegister(20)))
        print(reg21.assign(self.readRegister(21)))
        print(reg22.assign(self.readRegister(22)))
        #print(reg23.assign(self.readRegister(23)))
        print(reg24.assign(self.readRegister(24)))
        print(reg25.assign(self.readRegister(25)))
        print(reg26.assign(self.readRegister(26)))
        print(reg27.assign(self.readRegister(27)))
        print(reg28.assign(self.readRegister(28)))
        print(reg31.assign(self.readRegister(31)))

