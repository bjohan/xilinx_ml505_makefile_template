COMPONENTS = $(wildcard component_*.py)
TESTS = $(wildcard test_*.py)
VCDS = $(TESTS:.py=.vcd)
NAMES_WITH_SUFFIX = $(patsubst component_%,% ,$(COMPONENTS))
VHDLS = $(patsubst %.py, %.vhd, $(NAMES_WITH_SUFFIX))

#$(info $(COMPONENTS))

SIMULATION_SOURCES = $(wildcard simulation_*.py)
SIMULATION_VCDS = $(SIMULATION_SOURCES:.py=.vcd)

INTERACTIVE_SOURCES = $(wildcard interactive_*.py)
INTERACTIVE_VCDS = $(INTERACTIVE_SOURCES:.py=.vcd)

PYTHON = ./pyenv/bin/python3


$(PYTHON):
	mkdir -p pyenv
	python3 -m venv pyenv
	pyenv/bin/pip install git+https://github.com/myhdl/myhdl.git@master
	pyenv/bin/pip install getchar
	pyenv/bin/pip install bitstring

.DELETE_ON_ERROR:

test_%.vcd: test_%.py component_%.py $(PYTHON)
	$(PYTHON) $<
	rm -f $(@:.vcd=.*.*.vcd)

%.vhd: generate_vhdl_%.py component_%.py $(PYTHON)
	$(PYTHON) $<

simulation_%.vcd: simulation_%.py $(PYTHON)
	$(PYTHON) $<
	rm -f $(@:.vcd=.*.*.vcd)

interactive_%.vcd: interactive_%.py client_%.py $(PYTHON) $(COMPONENTS)
	$(PYTHON) $<&
	sleep 0.5
	$(PYTHON) $(word 2, $^)
	rm -f $(@:.vcd=.*.*.vcd)
    

.PHONY: clean simuations vhdls tests all
tests: $(VCDS)

vhdls: $(VHDLS)

simulations: $(SIMULATION_VCDS)

interactives: $(INTERACTIVE_VCDS)

all: tests vhdls simulations# interactives

clean:
	rm -f $(VCDS) $(VHDLS) $(SIMULATION_VCDS) $(INTERACTIVE_VCDS) pck_myhdl_011.vhd

clean_pyenv:
	rm -rf pyenv
	
