from myhdl import *
from component_trigged_counter import trigged_counter

def convert_trigged_counter(hdl):
	reset = ResetSignal(0, active=0, isasync=True)
	clk = Signal(False)
	output = Signal(intbv(0)[8:])
	count = Signal(False)
	trigged_counter_inst=trigged_counter(reset, clk, count, output)
	trigged_counter_inst.convert(hdl=hdl);

convert_trigged_counter(hdl='VHDL')
