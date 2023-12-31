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
VERILOGS = $(wildcard *.v)

UCF = ml505_board.ucf
TARGET = output
TOP = template_project_top

define XST_SYNTH_OPTS
-ifn $(TARGET).prj
-ifmt mixed
-ofn $(TARGET)
-ofmt NGC
-p $(PART)-$(SPEED)-$(PACKAGE)
-top $(TOP)
-opt_mode Speed
-opt_level 1
-power NO
-iuc NO
-keep_hierarchy No
-netlist_hierarchy As_Optimized
-rtlview Yes
-glob_opt AllClockNets
-read_cores YES
-write_timing_constraints NO
-cross_clock_analysis NO
-hierarchy_separator /
-bus_delimiter <>
-case Maintain
-slice_utilization_ratio 100
-bram_utilization_ratio 100
-dsp_utilization_ratio 100
-lc Off
-reduce_control_sets Off
-verilog2001 YES
-fsm_extract YES -fsm_encoding Auto
-safe_implementation No
-fsm_style LUT
-ram_extract Yes
-ram_style Auto
-rom_extract Yes
-mux_style Auto
-decoder_extract YES
-priority_extract Yes
-shreg_extract YES
-shift_extract YES
-xor_collapse YES
-rom_style Auto
-auto_bram_packing NO
-mux_extract Yes
-resource_sharing YES
-async_to_sync NO
-use_dsp48 Auto
-iobuf YES
-max_fanout 100000
-bufg 32
-register_duplication YES
-register_balancing No
-slice_packing YES
-optimize_primitives NO
-use_clock_enable Auto
-use_sync_set Auto
-use_sync_reset Auto
-iob Auto
-equivalent_register_removal YES
-slice_utilization_ratio_maxmargin 5
endef
export XST_SYNTH_OPTS

define BITGEN_OPTS
-w
-g DebugBitstream:No
-g Binary:no
-g CRC:Enable
-g ConfigRate:2
-g CclkPin:PullUp
-g M0Pin:PullUp
-g M1Pin:PullUp
-g M2Pin:PullUp
-g ProgPin:PullUp
-g DonePin:PullUp
-g InitPin:Pullup
-g CsPin:Pullup
-g DinPin:Pullup
-g BusyPin:Pullup
-g RdWrPin:Pullup
-g HswapenPin:PullUp
-g TckPin:PullUp
-g TdiPin:PullUp
-g TdoPin:PullUp
-g TmsPin:PullUp
-g UnusedPin:PullDown
-g UserID:0xFFFFFFFF
-g ConfigFallback:Enable
-g SelectMAPAbort:Enable
-g BPI_page_size:1
-g OverTempPowerDown:Disable
-g USR_ACCESS:None
-g JTAG_SysMon:Enable
-g DCIUpdateMode:AsRequired
-g StartUpClk:CClk
-g DONE_cycle:4
-g GTS_cycle:5
-g GWE_cycle:6
-g LCK_cycle:NoWait
-g Match_cycle:Auto
-g Security:None
-g DonePipe:No
-g DriveDone:No
-g Encrypt:No
endef
export BITGEN_OPTS

define COREGEN_OPTS
ET addpads = false
SET asysymbol = true
SET busformat = BusFormatAngleBracketNotRipped
SET createndf = false
SET designentry = VHDL
SET device = $(PART)
SET devicefamily = $(FAMILY)
SET flowvendor = Other
SET formalverification = false
SET foundationsym = false
SET implementationfiletype = Ngc
SET package = $(PACKAGE)
SET removerpms = false
SET simulationfiles = Behavioral
SET speedgrade = -$(SPEED)
SET verilogsim = false
SET vhdlsim = true
SET workingdirectory = ./tmp/
endef
export COREGEN_OPTS

PAF = $(TARGET)_plan_ahead_project_init.tcl
CGF = $(TARGET)_coregen.cgp

myhdls:
	$(MAKE) -C myhdl vhdls

$(TARGET).prj : $(VHDLS) $(VERILOGS) myhdls
	@truncate -s0 $(TARGET).prj
	@for i in $(VERILOGS); do echo verilog work '"'$$i'"' >> $(TARGET).prj; done
	@for i in $(VHDLS); do echo vhdl work '"'$$i'"' >> $(TARGET).prj; done
	@for i in $(wildcard myhdl/*.vhd); do echo vhdl work '"'$$i'"' >> $(TARGET).prj; done

$(TARGET).xst : Makefile $(TARGET).prj
	@truncate -s0 $(TARGET).xst
	@echo set -tmpdir "xst/projnav.tmp" >> $(TARGET).xst
	@echo set -xsthdpdir "xst" >> $(TARGET).xst
	@echo run >> $(TARGET).xst
	@echo "$$XST_SYNTH_OPTS)" >> $(TARGET).xst

xst : 
	mkdir -p xst

xst/projnav.tmp : xst
	mkdir -p xst/projnav.tmp

#synthesize
$(TARGET).syr $(TARGET).ngc : $(TARGET).xst xst xst/projnav.tmp
	$(call run_xilinx_environment,xst -intstyle ise -ifn $(TARGET).xst -ofn $(TARGET).syr)


#translate
$(TARGET).ngd : $(TARGET).syr $(TARGET).ngc $(UCF)
	$(call run_xilinx_environment, ngdbuild -intstyle ise -dd _ngo -nt timestamp -uc $(UCF) -p $(PART)-$(PACKAGE)-$(SPEED) $(TARGET).ngc $(TARGET).ngd)

#map
$(TARGET)_map.ncd : $(TARGET).ngd
	$(call run_xilinx_environment,map -p $(PART)-$(PACKAGE)-$(SPEED) -w -logic_opt off -ol high -t 1 -register_duplication off -global_opt off -mt off -cm area -ir off -power off -o $(TARGET)_map.ncd $(TARGET).ngd $(TARGET).pcf)

#place and route
$(TARGET).ncd : $(TARGET)_map.ncd
	$(call run_xilinx_environment,par -w -intstyle ise -ol high -mt off $(TARGET)_map.ncd $(TARGET).ncd, $(TARGET).pcf)

$(TARGET).ut:
	echo "$$BITGEN_OPTS" > $(TARGET).ut

#timing report
$(TARGET).twx $(TARGET).twr : $(TARGET).ncd
	$(call run_xilinx_environment,trce -intstyle ise -v 3 -s $(SPEED) -n 3 -fastpaths -xml $(TARGET).twx $(TARGET).ncd -o $(TARGET).twr $(TARGET).pcf)

#programming file
$(TARGET).bit : $(TARGET).ut $(TARGET).ncd
	$(call run_xilinx_environment,bitgen -intstyle ise -f $(TARGET).ut $(TARGET).ncd)


$(PAF) : $(TARGET).syr $(UCF) $(TARGET).twx $(TARGET).ncd
	@echo "start_gui" > $(PAF)
	@echo "create_project tmp_proj /tmp/tmp_proj -part $(PART) -force" >> $(PAF)
	@echo "set_property design_mode GateLvl [current_fileset]" >> $(PAF)
	@echo "add_files -norecurse $(TARGET).ngc" >> $(PAF)
	@echo "import_files -force -norecurse" >> $(PAF)
	@echo "import_files -fileset constrs_1 -force -norecurse $(UCF)" >> $(PAF)
	@echo "import_as_run -run impl_1 -twx $(TARGET).twx $(TARGET).ncd" >> $(PAF)
	#@echo "open_run impl_1" >> $(PAF)
	#@echo "reset_run impl_1" >> $(PAF)
	#@echo "launch_runs impl_1" >> $(PAF)
	#@echo "wait_on_run impl_1" >> $(PAF)
	#@echo "report_drc -name drc_1" >> $(PAF)

plan_ahead : $(PAF)
	$(call run_xilinx_environment, planAhead -source $(PAF))


$(CGF): 
	echo "$$COREGEN_OPTS" > $(CGF)

coregen : $(CGF)
	$(call run_xilinx_environment, coregen -p $(CGF))

fpga_target : $(TARGET).bit
	djtgcfg prog -d JtagHs1 -i 4 -f $(TARGET).bit

all: $(TARGET).bit $(TARGET).twr
clean:
	rm -f $(TARGET).prj $(TARGET).xst $(TARGET).syr $(TARGET).ngc $(TARGET).bld $(TARGET).ngd $(TARGET).ngr $(TARGET)_xst.xrpt $(TARGET)_ngdbuild.xrpt $(TARGET)_map.map  $(TARGET)_map.mrp $(TARGET)_map.ncd $(TARGET)_map.ngm $(TARGET).pcf $(TARGET)_summary.xml $(TARGET)_usage.xml $(TARGET).ncd $(TARGET).pad $(TARGET).par $(TARGET).ptwx $(TARGET).unroutes $(TARGET).xpi $(TARGET)_pad.csv $(TARGET)_pad.txt $(TARGET).bgn $(TARGET).bit $(TARGET).drc $(TARGET).ut usage_statistics_webtalk.html webtalk.log $(TARGET)_bitgen.xwbt $(TARGET).twr $(TARGET).twx $(TARGET)_plan_ahead_project_init.tcl planAhead.jou planAhead.log
	rm -rf xlnx_auto_0_xdb xst/projnav.tmp xst _xmsgs _ngo
	rm -f *.lso *.xrpt
