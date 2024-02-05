from myhdl import *
from interface_axi4s import Axi4sInterface


from component_function_debug_core import function_debug_core

def convert_function_debug_core(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    i = Axi4sInterface(32); 
    o = Axi4sInterface(32);
    debug = Signal(modbv(0)[123:]) 

    function_debug_core_inst = function_debug_core(reset, clk, i, o, debug, 64)
    function_debug_core_inst.convert(hdl=hdl);


convert_function_debug_core(hdl='VHDL')
