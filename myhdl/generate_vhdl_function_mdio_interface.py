from myhdl import *
from interface_axi4s import Axi4sInterface


from component_function_mdio_interface import function_mdio_interface

def convert_function_mdio_interface(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    i = Axi4sInterface(32); 
    o = Axi4sInterface(32);
    
    mdio_in = Signal(False)
    mdio_out = Signal(False)
    mdio_tristate = Signal(False)
    mdio_clk = Signal(False)

    function_mdio_interface_inst = function_mdio_interface(reset, clk, i, o, mdio_in, mdio_out, mdio_tristate, mdio_clk)
    function_mdio_interface_inst.convert(hdl=hdl);


convert_function_mdio_interface(hdl='VHDL')
