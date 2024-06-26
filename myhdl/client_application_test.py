from tcp import TcpClient
from functions.interface import FunctionInterface
import queue

print("Creating client")
cli = TcpClient("localhost", 8080)
print("Getting interface")
iface = FunctionInterface(cli, cli)
print("Interface created")
try:

    mdio = iface.frameMapper.functionMap[b'\x05']
    print("Setting phy address")
    mdio.setPhyAddr(7)
    print("Setting up debug core")
    dbg2 = iface.frameMapper.functionMap[b'\x03']
    dbg2.setReferenceWord('1000')
    dbg2.setCareMask('1000')
    dbg2.setArm()
    print("Reading phy registers")
    print(mdio.readRegister(1))
    print(mdio.writeRegister(1, 0x137f))
    print("Waiting for debugdata")
    dbg2.receiveData()
    dbg2.dumpVcd('mdio.vcd')

    #mdio = iface.frameMapper.functionMap[b'\x05']
    #print(mdio.readRegister(3, 1))
    #print(mdio.writeRegister(4, 2, 0x137f))
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
except (KeyboardInterrupt, queue.Empty):
    print("Exception in client")
    pass
print("Shutting down interface")
iface.stop()
