from myhdl import *


from component_rs232rx import rs232rx

def convert_rs232rx(hdl):
    clk = Signal(False)
    toTx = Signal(intbv(0x00, min=0, max=256))
    rxdata = Signal(intbv(0x00, min=0, max=256))
    baudDiv = Signal(intbv(min=0, max=2**24))
    txValid = Signal(False)
    rxValid = Signal(False)
    txReady = Signal(False)
    txd = Signal(True)
    reset = ResetSignal(0, active=0, isasync=True)
    rs232rx_inst=rs232rx(reset, rxdata, rxValid, txd, clk, baudDiv);
    rs232rx_inst.convert(hdl=hdl);


convert_rs232rx(hdl='VHDL')
