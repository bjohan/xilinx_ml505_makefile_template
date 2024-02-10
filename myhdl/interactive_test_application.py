from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_test_application_str import test_application_str
from simutil_component_tcp_rx import tcp_rx
from simutil_component_tcp_tx import tcp_tx
from tcp import TcpServer
dataToWrite = [   0xFF,                                            0x01, 0xAB, 0xAC]
writeDelays = [   0,                                               4,    0,    0,  ]
writeLast   = [   1,                                               0,    0,    1,  ]

dataToRead = [    0xFF, 0x01, 0xFF,                                0x01, 0xAB, 0xAC]
readDelays = [    0,    0,    0,                                   0,    0,    0]
readLast   = [    1,    0,    1,                                   0,    0,    1]

@block
def test_test_application_str(conn):
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    streamIn = Axi4sInterface(8)
    streamOut = Axi4sInterface(8) 
    i_stdin = tcp_rx(reset, clk, streamIn, conn)
    test_application_str_inst = test_application_str(reset, clk, streamIn, streamOut )
    i_stdout = tcp_tx(reset, clk, streamOut, conn)

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    @instance
    def monitor():
        for i in range(1000000):
            yield clk.posedge
        print("Simulation did not end successfully")
        quit(-1)

    @instance
    def gen_reset():
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = 0
        yield clk.posedge

    #@instance
    #def read():
    #    streamOut.ready.next = 1
    #    yield clk.posedge
    #    yield reset.negedge
    #    yield tbReceiveSequence(clk, streamOut, dataToRead, readLast, readDelays);
    #    raise StopSimulation("Simulation ended successfully")

    #@instance
    #def write():
    #    yield reset.negedge
    #    yield tbTransmitSequence(clk, streamIn, dataToWrite, writeLast, writeDelays);


    return clkgen, gen_reset, monitor, test_application_str_inst, i_stdin, i_stdout#, read

srv = TcpServer("localhost", 8080)
print("Started server waiting for connection")
conn = srv.getConnection()
print("Got connection, starting simulation")
tb = test_test_application_str(conn);
tb.config_sim(trace=True)
tb.run_sim();
