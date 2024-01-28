from myhdl import *
from interface_axi4s import Axi4sInterface

from component_test_application_str import test_application_str

def convert_axi4s_test_application_str(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    streamIn = Axi4sInterface(8)
    streamOut = Axi4sInterface(8) 

    test_application_str_inst = test_application_str(reset, clk, streamIn, streamOut )

    test_application_str_inst.convert(hdl=hdl);


convert_axi4s_test_application_str(hdl='VHDL')
