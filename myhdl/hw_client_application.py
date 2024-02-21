import serial
from functions.interface import FunctionInterface
import time
import random
print("Creating client")
cli = serial.Serial('/dev/ttyUSB0', 115200, timeout=1) 
#cli.write(b"\xc0\x030123456789")
#print(cli.read(10))
#quit()
iface = FunctionInterface(cli, cli)
print("Interface created")
try:
    mdio = iface.frameMapper.functionMap[b'\x05']
    dbg2 = iface.frameMapper.functionMap[b'\x03']
    dbg2.setReferenceWord('1000')
    dbg2.setCareMask('1000')
    dbg2.setArm()
    #for rr in random.sample(range(32), 32):
    #    print("register", rr, "value", mdio.readRegister(7, rr))
    #    time.sleep(0.1)
    print(mdio.readRegister(7, 1))
    print(mdio.writeRegister(7, 2, 0x137f))
    dbg2.dumpVcd('mdio.vcd')
    for rr in range(32):
        print("register", rr, "value", mdio.readRegister(7, rr))

    #mdio = iface.frameMapper.functionMap[b'\x05']
    #phyAddr = 7
    #print("Reading register 1")
    #print(mdio.readRegister(phyAddr, 1))
    #print("Writing register 1")
    #mdio.writeRegister(phyAddr, 2, 0x137f)
    #print("Reading register 1")
    #print(mdio.readRegister(phyAddr, 1))

    #print("Arming and reading debug core 0")
    #dbg = iface.frameMapper.functionMap[b'\x01']
    #dbg.setAndMask('1'*73)
    #dbg.setOrMask('1'*73)
    #dbg.setArm()
    #dbg.dumpVcd('test1.vcd')

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
