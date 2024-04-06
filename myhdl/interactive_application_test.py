from myhdl import *
from interface_axi4s import Axi4sInterface, tbTransmitSequence, tbReceiveSequence
from component_application_test_str import application_test_str
from component_axi4s_last_deescaper import axi4s_last_deescaper
from component_axi4s_last_escaper import axi4s_last_escaper
from component_rs232rx import rs232rx
from component_rs232tx import rs232tx
from simutil_component_tcp_rx import tcp_rx
from simutil_component_tcp_tx import tcp_tx
from tcp import TcpServer

@block
def serialrtx(reset, clk, i, o, baudDiv=100):
    wire = Signal(False)
    tx = rs232tx(reset, clk, i, wire, baudDiv)
    rx = rs232rx(reset, clk, o, wire, baudDiv)
    return rx, tx

@block
def interactive_application_test(conn):
    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    frameError = Signal(False)
 
    streamIn = Axi4sInterface(8)
    #streamInLimited = Axi4sInterface(8)
    streamInDeescaped = Axi4sInterface(8)
    streamOut = Axi4sInterface(8) 
    streamOutEscaped = Axi4sInterface(8)

    mdio_in = Signal(True)
    mdio_out = Signal(False)
    mdio_tristate = Signal(False)
    mdio_clk = Signal(False)

    debug0 = Signal(modbv(0)[16:])
    i_stdin = tcp_rx(reset, clk, streamIn, conn)
    #i_rate_limit_in = serialrtx(reset, clk, streamIn, streamInLimited)
    i_axi4s_last_deescaper = axi4s_last_deescaper(reset, clk, streamIn, streamInDeescaped, frameError, 0xc0, 0x03)
    application_test_str_inst = application_test_str(reset, clk, streamInDeescaped, streamOut, mdio_in, mdio_out, mdio_tristate, mdio_clk, debug0)
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
        for i in range(100000):
            yield clk.posedge
        raise StopSimulation("Simulation did not end successfully")
        #print("Simulation did not end successfully")
        #quit(-1)

    @instance
    def gen_reset():
        reset.next = 1
        for i in range(3):
            yield clk.posedge
        reset.next = 0
        yield clk.posedge

    return clkgen, gen_reset, monitor, application_test_str_inst, i_stdin, i_stdout, i_axi4s_last_deescaper, i_axi4s_last_escaper#, i_rate_limit_in#, read

srv = TcpServer("localhost", 8080)
print("Started server waiting for connection")
conn = srv.getConnection()
conn.conn.settimeout(0)
print("Got connection, starting simulation")
tb = interactive_application_test(conn);
tb.config_sim(trace=True)
tb.run_sim();
print("Simulation done, closing server")
conn = None
srv = None
print("Shutdown complete")


