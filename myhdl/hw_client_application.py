import serial
from functions.interface import FunctionInterface
import time
import random
import bitstring
print("Creating client")
cli = serial.Serial('/dev/ttyUSB0', 115200, timeout=1) 
#cli.write(b"\xc0\x030123456789")
#print(cli.read(10))
#quit()
iface = FunctionInterface(cli, cli)
print("Interface created")
def intToReadableBinaryString(n):
    s = '{0:016b}'.format(n)
    s2 = ''
    for i in range(4):
        s2+=s[:4]+' '
        s=s[4:]
    return s2

try:
    mdio = iface.frameMapper.functionMap[b'\x05']
    mdio.setPhyAddr(7)
    dbg2 = iface.frameMapper.functionMap[b'\x03']
    #dbg2.setReferenceWord('1000')
    #dbg2.setCareMask('1000')
    #dbg2.setArm()
    #for rr in random.sample(range(32), 32):
    #    print("register", rr, "value", mdio.readRegister(7, rr))
    #    time.sleep(0.1)
    print(mdio.readRegister(1))
    print(mdio.writeRegister(2, 0x137f))
    #dbg2.dumpVcd('mdio.vcd')
    for rr in range(32):
        bv = mdio.readRegister(rr)
        print("register", rr, "value", bv, intToReadableBinaryString(bv))

    mdio.printConfig()
    #mdio = iface.frameMapper.functionMap[b'\x05']
    #phyAddr = 7
    #print("Reading register 1")
    #print(mdio.readRegister(phyAddr, 1))
    #print("Writing register 1")
    #mdio.writeRegister(phyAddr, 2, 0x137f)
    #print("Reading register 1")
    #print(mdio.readRegister(phyAddr, 1))

    print("Arming and reading debug core 0")
    dbg = iface.frameMapper.functionMap[b'\x01']
    dbg.setReferenceWord('0000000000000001')
    dbg.setCareMask('0000000000000001')
    dbg.setArm()
    dbg.dumpVcd('enet.vcd')

    #print("Arming and reading debug core 1")
    #dbg2 = iface.frameMapper.functionMap[b'\x03']
    #dbg2.setAndMask('1'*13)
    #dbg2.setOrMask('1'*13)
    #dbg2.setArm()
    #dbg2.dumpVcd('test2.vcd')

    #print("Arming and reading debug core 0 again")
    #dbg.setArm()
    #dbg.dumpVcd('test3.vcd')
    #print("Done")
except KeyboardInterrupt:
    pass
print("Shutting down interface")
iface.stop()
