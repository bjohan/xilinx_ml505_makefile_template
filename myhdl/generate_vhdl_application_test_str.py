from myhdl import *
from interface_axi4s import Axi4sInterface

from component_application_test_str import application_test_str

def convert_axi4s_application_test_str(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    streamIn = Axi4sInterface(8)
    streamOut = Axi4sInterface(8) 

    mdio_in = Signal(True)
    mdio_out = Signal(False)
    mdio_tristate = Signal(False)
    mdio_clk = Signal(False)

    application_test_str_inst = application_test_str(reset, clk, streamIn, streamOut, mdio_in, mdio_out, mdio_tristate, mdio_clk)

    application_test_str_inst.convert(hdl=hdl);


convert_axi4s_application_test_str(hdl='VHDL')
