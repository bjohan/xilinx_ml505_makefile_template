from myhdl import *

t_State = enum('S_SHIFTING', 'S_WAIT_LAST', 'S_TRANSFER_OUT');

@block
def axi4s_unpacker(reset, clk, i, out_regs_o,outw, out_valid_o, readyIn):
    num = int(len(out_regs_o)/outw)
    stat = Signal(t_State.S_SHIFTING)
    n = Signal(intbv(0, min=0, max = num+1))
    readyOut = Signal(False)
    out_regs = Signal(intbv(0)[len(out_regs_o):])
    out_valid = Signal(False)

    @always_comb
    def shadow_regs():
        i.ready.next = readyOut
        out_regs_o.next = out_regs
        out_valid_o.next = out_valid

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if stat == t_State.S_SHIFTING:
            readyOut.next = 1
            if i.valid and readyOut and n != num:
                for j in range(num-1):
                    topBit = (j+2)*outw
                    midBit = (j+1)*outw
                    lowBit = (j)*outw
                    out_regs.next[midBit:lowBit] = out_regs[topBit:midBit]
                out_regs.next[outw*num:outw*(num-1)]=i.data
                n.next = n.next + 1
                if n == num-1:
                    stat.next = t_State.S_WAIT_LAST
                    if i.last:
                        readyOut.next = 0
                        stat.next = t_State.S_TRANSFER_OUT

        if stat == t_State.S_WAIT_LAST:
            if i.valid and readyOut and i.last:
                readyOut.next = 0
                n.next = 0
                out_valid.next = 1
                stat.next = t_State.S_TRANSFER_OUT
            
        if stat == t_State.S_TRANSFER_OUT:
            if out_valid and readyIn:
                out_valid.next = 0
                readyOut.next = 1
                stat.next = t_State.S_SHIFTING
    return logic, shadow_regs
