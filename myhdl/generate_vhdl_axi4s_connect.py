from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_connect import axi4s_connect

def convert_axi4s_connect(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    i = Axi4sInterface(8); 
    o = Axi4sInterface(8); 

    axi4s_connect_inst = axi4s_connect(i, o)
    axi4s_connect_inst.convert(hdl=hdl);


convert_axi4s_connect(hdl='VHDL')
