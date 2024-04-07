from myhdl import *

t_State = enum('S_SHIFTING', 'S_TRANSFER_TAIL', 'S_SHIFT_REST', 'S_TRANSFER_OUT');

@block
def axi4s_head_unpacker(reset, clk, i, tail_out, out_regs_o, out_valid_o, readyIn, words):
    num = int(len(out_regs_o)/len(i.data))
    stat = Signal(t_State.S_SHIFTING)
    n = Signal(intbv(0, min=0, max = num+1))
    readyOut = Signal(False)
    out_regs = Signal(modbv(0)[len(out_regs_o):])
    out_valid = Signal(False)
    hasTail = Signal(False)
    inToTail = Signal(False)

    @always_comb
    def shadow_regs():
        out_regs_o.next = out_regs
        out_valid_o.next = out_valid

        if inToTail:
            tail_out.data.next = i.data
            tail_out.valid.next = i.valid
            tail_out.last.next = i.last
            i.ready.next = tail_out.ready
        else:
            i.ready.next = readyOut
            tail_out.valid.next = 0

    @always_seq(clk.posedge, reset=reset)
    def logic():
        if stat == t_State.S_SHIFTING:
            hasTail.next = 0
            readyOut.next = 1
            if i.valid and readyOut and n != num:
                if i.last:
                    readyOut.next = 0
                    stat.next = t_State.S_SHIFT_REST
                out_regs.next = out_regs.next >> len(i.data) | i.data << ((num-1)*len(i.data))
                n.next = n + 1
                words.next = n + 1
                if n == num-1:
                    hasTail.next = not i.last
                    readyOut.next = 0
                    out_valid.next = 1
                    stat.next = t_State.S_TRANSFER_OUT

        if stat == t_State.S_TRANSFER_OUT:
            if out_valid and readyIn:
                out_valid.next = 0
                readyOut.next = 1
                n.next = 0
                words.next = 0
                if hasTail:
                    inToTail.next = 1
                    stat.next=t_State.S_TRANSFER_TAIL
                else:
                    stat.next = t_State.S_SHIFTING

        if stat == t_State.S_TRANSFER_TAIL:
            if i.valid and tail_out.ready and i.last:
                readyOut.next = 0
                n.next = 0
                inToTail.next = 0
                stat.next = t_State.S_SHIFTING
            
        if stat == t_State.S_SHIFT_REST:
            out_regs.next = out_regs.next >> len(i.data) 
            if n == num-1:
                out_valid.next = 1
                stat.next = t_State.S_TRANSFER_OUT
            else:
                n.next = n+1

    return logic, shadow_regs
