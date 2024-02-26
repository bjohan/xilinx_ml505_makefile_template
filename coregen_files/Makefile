#Set ISE_ATH to where your ISE is installed
ISE_PATH = /home/bjohan/opt/xilinx/14.7/ISE_DS
ISE_SETUP = $(ISE_PATH)/settings64.sh
define run_xilinx_environment
	@echo running \"$1\" in xilinx environmet
	bash -c 'source $(ISE_SETUP) ; $(1)'
endef

FAMILY=virtex5
PART = xc5vlx50t#-1-ff1136
SPEED =1
PACKAGE=ff1136
VHDLS = $(wildcard *.vhdl) $(wildcard *.vhd)
COREGENPROJS = $(wildcard *.cgp)
NAMES = $(basename $(COREGENPROJS))
VHDLS = $(addsuffix .vhd, $(NAMES))


%.vhd : %.cgp %.xco
	$(call run_xilinx_environment, coregen -b $(word 2, $^) -p $(word 1, $^))

all: $(VHDLS)
clean:
	rm -rf $(NAMES) tmp xlnx_auto_0_xdb
	rm -f $(NAMES:=.asy) $(NAMES:=.cgc) $(NAMES:=_flist.txt) $(NAMES:=.gise) $(NAMES:=.ngc) $(NAMES:=.vhd) $(NAMES:=.vho) $(NAMES:=.xise) $(NAMES:=_xmdf.tcl )coregen.log
