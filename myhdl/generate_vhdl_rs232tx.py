from myhdl import *


from component_rs232tx import rs232tx


#clk = Signal(False)
#toTx = Signal(intbv(0x00, min=0, max=256))
#rxdata = Signal(intbv(0x00, min=0, max=256))
#baudDiv = Signal(intbv(min=0, max=2**24))
#txValid = Signal(False)
#txReady = Signal(False)
#txd = Signal(True)
#reset = Signal(False)
#rs232tx_inst = toVHDL(rs232tx, reset, toTx, txValid, txReady, txd, clk, baudDiv);


def convert_rs232tx(hdl):
	clk = Signal(False)
	toTx = Signal(intbv(0x00, min=0, max=256))
	rxdata = Signal(intbv(0x00, min=0, max=256))
	baudDiv = Signal(intbv(min=0, max=2**24))
	txValid = Signal(False)
	txReady = Signal(False)
	txBusy = Signal(False)
	txd = Signal(True)
	reset = ResetSignal(0, active=1, isasync=False)
	rs232tx_inst=rs232tx(reset, toTx, txValid, txReady, txBusy, txd, clk, baudDiv)
	rs232tx_inst.convert(hdl=hdl);

convert_rs232tx(hdl='VHDL')
