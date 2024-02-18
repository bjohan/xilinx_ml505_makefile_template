from tcp import TcpClient
from functions.interface import FunctionInterface

print("Creating client")
cli = TcpClient("localhost", 8080)
iface = FunctionInterface(cli, cli)
print("Interface created")
try:
    print("Arming and reading debug core 0")
    dbg = iface.frameMapper.functionMap[b'\x01']
    dbg.setAndMask('1'*73)
    dbg.setOrMask('1'*73)
    dbg.setArm()
    dbg.dumpVcd('test1.vcd')

    print("Arming and reading debug core 1")
    dbg2 = iface.frameMapper.functionMap[b'\x03']
    dbg2.setAndMask('1'*13)
    dbg2.setOrMask('1'*13)
    dbg2.setArm()
    dbg2.dumpVcd('test2.vcd')

    print("Arming and reading debug core 0 again")
    dbg.setArm()
    dbg.dumpVcd('test3.vcd')
    print("Done")
except KeyboardInterrupt:
    pass
print("Shutting down interface")
iface.stop()
