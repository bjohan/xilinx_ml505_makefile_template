from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_test_application_str import test_application_str
from component_axi4s_last_deescaper import axi4s_last_deescaper
from component_axi4s_last_escaper import axi4s_last_escaper
from simutil_component_tcp_rx import tcp_rx
from simutil_component_tcp_tx import tcp_tx
from tcp import TcpServer

@block
def interactive_test_application(conn):
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    frameError = Signal(False)
 
    streamIn = Axi4sInterface(8)
    streamInDeescaped = Axi4sInterface(8)
    streamOut = Axi4sInterface(8) 
    streamOutEscaped = Axi4sInterface(8)

    i_stdin = tcp_rx(reset, clk, streamIn, conn)
    i_axi4s_last_deescaper = axi4s_last_deescaper(reset, clk, streamIn, streamInDeescaped, frameError, 0xc0, 0x03)
    test_application_str_inst = test_application_str(reset, clk, streamInDeescaped, streamOut)
    i_axi4s_last_escaper = axi4s_last_escaper(reset, clk, streamOut, streamOutEscaped, 0xc0, 0x03)
    i_stdout = tcp_tx(reset, clk, streamOutEscaped, conn)

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    @instance
    def monitor():
        for i in range(10000):
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

    return clkgen, gen_reset, monitor, test_application_str_inst, i_stdin, i_stdout, i_axi4s_last_deescaper, i_axi4s_last_escaper#, read

srv = TcpServer("localhost", 8080)
print("Started server waiting for connection")
conn = srv.getConnection()
conn.conn.settimeout(0)
print("Got connection, starting simulation")
tb = interactive_test_application(conn);
tb.config_sim(trace=True)
tb.run_sim();
