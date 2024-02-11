from myhdl import *
from interface_axi4s import Axi4sInterface


from component_axi4s_address_branch import axi4s_address_branch

def convert_axi4s_address_branch(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    i_prev = Axi4sInterface(8); 
    o_prev = Axi4sInterface(8);
    i_func = Axi4sInterface(8); 
    o_func = Axi4sInterface(8);
    i_next = Axi4sInterface(8); 
    o_next = Axi4sInterface(8);
 
    axi4s_address_branch_inst = axi4s_address_branch(reset, clk, i_prev, o_prev, i_func, o_func, 0x44, i_next, o_next)
    axi4s_address_branch_inst.convert(hdl=hdl);


convert_axi4s_address_branch(hdl='VHDL')
