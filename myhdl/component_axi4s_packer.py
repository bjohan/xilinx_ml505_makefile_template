from myhdl import *

t_State = enum('S_GET_INPUT', 'S_SHIFTING', 'S_WAIT_LAST', 'S_TRANSFER_OUT');

@block
def axi4s_packer(reset, clk, o, in_regs, in_valid ,in_ready_o, txOne):
    num = int(len(in_regs)/len(o.data))
    state = Signal(t_State.S_GET_INPUT)
    n = Signal(intbv(0, min=0, max = num+1))
    nToTx = Signal(intbv(0, min=0, max = num+1)) 
    in_regs_r = Signal(intbv(0)[len(in_regs):])

    in_ready = Signal(True)
    out_valid = Signal(False)

    @always_comb
    def shadow_regs():
        in_ready_o.next = in_ready

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if state == t_State.S_GET_INPUT:
            o.last.next = 0
            o.valid.next = 0
            if in_ready and in_valid:
                if txOne:
                    nToTx.next = 1
                else:
                    nToTx.next = num
                in_regs_r.next = in_regs
                in_ready.next = 0
                state.next = t_State.S_SHIFTING
                o.data.next = in_regs_r.next[len(o.data):0]
                o.valid.next = 1
                o.last.next = txOne

        if state == t_State.S_SHIFTING:
            o.valid.next = 1
            if o.ready and n != nToTx:
                if n+1 == nToTx-1:
                    o.last.next = 1

                for j in range(nToTx-1):
                    topBit = (j+2)*len(o.data)
                    midBit = (j+1)*len(o.data)
                    lowBit = (j)*len(o.data)
                    in_regs_r.next[midBit:lowBit] = in_regs_r[topBit:midBit]
                o.data.next = in_regs_r.next[len(o.data):0]
                n.next = n.next + 1
                if n == nToTx-1:
                    state.next = t_State.S_GET_INPUT
                    in_ready.next = 1
                    o.valid.next = 0
                    o.last.next = 0
                    n.next = 0
                    
    return logic, shadow_regs
