from myhdl import *
from interface_axi4s import Axi4sInterface

from component_application_test_str import application_test_str

def convert_axi4s_application_test_str(hdl):
    clk = Signal(False)
    reset = ResetSignal(False, active=1, isasync=False)
    
    streamIn = Axi4sInterface(8)
    streamOut = Axi4sInterface(8) 

    application_test_str_inst = application_test_str(reset, clk, streamIn, streamOut )

    application_test_str_inst.convert(hdl=hdl);


convert_axi4s_application_test_str(hdl='VHDL')
