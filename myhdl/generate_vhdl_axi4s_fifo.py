from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_fifo import axi4s_fifo

def convert_axi4s_fifo(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    i = Axi4sInterface(8); 
    o = Axi4sInterface(8); 

    axi4s_fifo_inst = axi4s_fifo(reset, clk, i, o, 1024)
    axi4s_fifo_inst.convert(hdl=hdl);


convert_axi4s_fifo(hdl='VHDL')
