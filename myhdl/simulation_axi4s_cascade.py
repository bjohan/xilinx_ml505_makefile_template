from myhdl import *


from component_axi4sn import axi4sn
from component_axi4sw import axi4sw
@block
def simulation_axi4s_cascade():

    clk = Signal(False)
    reset = ResetSignal(0, active=1, isasync=False)
    
    tDataIn = Signal(intbv(0xAA)[32:])
    tValidIn = Signal(False)
    tReadyOut = Signal(False)
    tLastIn = Signal(False)

    tData1 = Signal(intbv(0)[8:])
    tValid1 = Signal(False)
    tReady1 = Signal(False)
    tLast1 = Signal(False)

    tData2 = Signal(intbv(0)[32:])
    tValid2 = Signal(False)
    tReady2 = Signal(False)
    tLast2 = Signal(False)

    tDataOut = Signal(intbv(0)[8:])
    tValidOut = Signal(False)
    tReadyIn = Signal(True)
    tLastOut = Signal(False)

    transfer_in = Signal(False)
    transfer_1 = Signal(False)
    transfer_2 = Signal(False)
    transfer_out = Signal(False)

    @always_comb
    def transfers():
        transfer_in.next = tValidIn == 1 and tReadyOut == 1
        transfer_1.next = tValid1 == 1 and tReady1 == 1
        transfer_2.next = tValid2 == 1 and tReady2 == 1
        transfer_out.next = tValidOut == 1 and tReadyIn == 1

    @always(delay(10))
    def clkgen():
        if clk:
            clk.next = 0
        else:
            clk.next = 1

    axi4sn1_inst = axi4sn(reset, clk, tDataIn, tValidIn, tReadyOut, tLastIn, tData1, tValid1, tReady1, tLast1, 4)

    axi4sw1_inst = axi4sw(reset, clk, tData1, tValid1, tReady1, tLast1, tData2, tValid2, tReady2, tLast2, 4)
    axi4sn2_inst = axi4sn(reset, clk, tData2, tValid2, tReady2, tLast2, tDataOut, tValidOut, tReadyIn, tLastOut, 4)


    @instance
    def read():
        for i in range(3):
            yield clk.negedge
        while True:
            if not tValidOut:
                yield tValidOut.posedge
            yield clk.negedge
            tReadyIn.next = 1
            yield clk.negedge
            tReadyIn.next = 0
            yield clk.negedge
            tReadyIn.next = 1
            yield clk.negedge
            yield tValidOut.negedge
            yield tValidOut.posedge
            yield tValidOut.negedge
            yield clk.negedge
            tReadyIn.next = 0;

    @instance
    def write():
        print("Synchronous reset")
        reset.next = 1
        for i in range(3):
            yield clk.negedge
        reset.next = 0
        print("Waiting 3 clks")
        for i in range(3):
            yield clk.negedge
        print("Starting to transmit")
        for b in [0xA3A2A1A0, 0xB3B2B1B0, 0xC3C2C1C0, 0xD3D2D1D0, 0xE3D2D1E0, 0xF3F2F1F0]:
            print("Transmitting ", b)
            if b == 0xB3B2B1B0:
                tLastIn.next = 1
            else:
                tLastIn.next = 0
            tDataIn.next = b
            tValidIn.next = 1
            yield clk.negedge
            if not tReadyOut:
                print("Waiting for ready")
                yield tReadyOut.posedge
            yield clk.negedge
            tValidIn.next = 0
        print("extra clocks")
        for i in range(3):
            yield clk.negedge
        print("stop simulation")
        raise StopSimulation("Simulation stopped")

    return transfers, clkgen, axi4sn1_inst, axi4sw1_inst, axi4sn2_inst, write, read

tb = simulation_axi4s_cascade();
tb.config_sim(trace=True)
tb.run_sim();
