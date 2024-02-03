----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date:    13:53:04 12/23/2023 
-- Design Name: 
-- Module Name:    template_project_top - Behavioral 
-- Project Name: 
-- Target Devices: 
-- Tool versions: 
-- Description: 
--
-- Dependencies: 
--
-- Revision: 
-- Revision 0.01 - File Created
-- Additional Comments: 
--
----------------------------------------------------------------------------------
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;
use work.all;
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx primitives in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity template_project_top is
    Port (  a,b: in  STD_LOGIC_VECTOR (1 downto 0);
	    clk_in, rst_in : in std_logic;
	    agreatb, led_1, led_2, led_3, led_4 : out  STD_LOGIC;
            hdr_2 : out STD_LOGIC;
            hdr_4 : out STD_LOGIC;
            hdr_6 : out STD_LOGIC;
            serial2_tx : out STD_LOGIC;
	    serial2_rx : in STD_LOGIC;
            serial1_tx : out STD_LOGIC; --Connected to db9
	    serial1_rx : in STD_LOGIC --Connected to db9
);
end template_project_top;

architecture Behavioral of template_project_top is

	component clk
	port(
		clkin_in : in std_logic;
		RST_IN : in std_logic;
		CLKIN_IBUFG_OUT : out std_logic;
		CLKOUT0_OUT : out std_logic;
		LOCKED_OUT : out std_logic
	 );
	 end component;

	component rs232tx 
    	port (
        	reset: in std_logic;
        	toTx: in unsigned(7 downto 0);
        	txValid: in std_logic;
        	txReadyOut: out std_logic;
        	txBusy: out std_logic;
        	txd: out std_logic;
        	clk: in std_logic;
        	baudDiv: in unsigned(23 downto 0)
    	);
	end component;

	component rs232rx
    	port (
        	reset: in std_logic;
        	rxdata: out unsigned(7 downto 0);
        	rxValid: out std_logic;
        	rxd: in std_logic;
        	clk: in std_logic;
        	baudDiv: in unsigned(23 downto 0)
    	);
	end component;

	--constant toTx : unsigned(7 downto 0) := "01111110";--to_unsigned(65, 8);
	signal toTx : unsigned(7 downto 0);
	signal fromRx : unsigned(7 downto 0);
	signal p0, p1, p2 : std_logic;
	signal cnt : unsigned(24 downto 0);
	signal cnt2 : unsigned(24 downto 0);
	signal cnt3 : unsigned(24 downto 0);
	signal clk_usr : std_logic;
	signal clk_int : std_logic;
	signal rst : std_logic;
	signal rdy : std_logic;
	signal bsy : std_logic;
	signal cnt_last : std_logic;
	signal trig : std_logic;
	signal tx : std_logic;
	signal dataValid : std_logic;
	signal testData : unsigned(31 downto 0);
	signal testDataValid: std_logic;
	signal testDataReady : std_logic;
	signal testData2 : unsigned(31 downto 0);
	signal testData2Valid: std_logic;
	signal testData2Ready : std_logic;
	signal toTxData : unsigned(7 downto 0);
	signal toTxValid: std_logic;
	signal toTxReady : std_logic;
	--signal fifoDin : std_logic_vector(35 downto 0);
	--signal fifoDout : std_logic_vector(35 downto 0);
	signal fifoDin : unsigned(35 downto 0);
	signal fifoDout : unsigned(35 downto 0);
	signal fifoFull : std_logic;
	signal fifoEmpty : std_logic;
begin
	serial2_tx <= serial2_rx;
	--serial1_tx <= serial1_rx;
	--serial1_tx <= '0';
	serial1_tx <= tx;
	agreatb <= p0 or p1 or p2;
	p0 <= a(1) and (not b(1));
	p1 <= a(0) and (not b(1)) and (not b(0));
	p2 <= a(1) and a(0) and (not b(0));
	led_2 <= cnt(22);
	--hdr_2 <= serial1_rx;
	hdr_2 <= testDataValid;
	hdr_4 <= testDataReady;
	--hdr_4 <= trig; 
	led_3 <= '1';
	led_4 <= rst;
	hdr_6 <= tx;
	rst <= not rst_in;

	i_clk: clk
	port map (
		clkin_in => clk_in, 
    		RST_IN => rst, 
    		CLKIN_IBUFG_OUT=> clk_int, --(CLKIN_IBUFG_OUT), 
    		CLKOUT0_OUT => clk_usr, 
    		LOCKED_OUT => led_1
    	);

	i_rs232tx: rs232tx 
    	port map(
        	reset => rst,
		toTx => toTxData,
		txValid => toTxValid,
		txReadyOut => toTxReady,
        	--toTx => toTx,
        	--txValid => dataValid,
        	--txReadyOut => rdy,
		txBusy => bsy,
        	txd => tx,
        	clk => clk_usr,
        	baudDiv => to_unsigned(859, 24)
    	);

	i_rs232rx: rs232rx 
    	port map(
        	reset => rst,
        	rxdata => fromRx,
        	rxValid => dataValid,
        	rxd => serial1_rx,
        	clk => clk_usr,
        	baudDiv => to_unsigned(859, 24)
    	);

	i_axi4sw: entity work.axi4sw
	port map(
		reset => rst,
        	clk => clk_usr,
        	tDataIn => fromRx,
        	tValidIn => dataValid,
		tLastIn => '0',
        	--tReadyOut_o => ;
        	tDataOut => testData,
        	tValidOut_o => testDataValid,
        	tReadyIn => testDataReady
	);


	fifoDin(31 downto 0) <= testData;
	fifoDin(35 downto 32) <= "0000";

    i_fifo: entity work.fifo
    port map(
        reset => rst,
        clk => clk_usr,
        din => fifoDin,
        we => testDataValid,
        ready_o => testDataReady,
        dout => fifoDout,
        re => testData2Ready,
        valid_o => testData2Valid
    );
    

	testData2 <= fifoDout(31 downto 0);

	i_axi4sn: entity work.axi4sn
	port map(
		reset => rst,
        	clk => clk_usr,
        	tDataIn => testData2,
        	tValidIn => testData2Valid,
        	tReadyOut_o => testData2Ready,
		tLastIn => '0',
        	tDataOut => toTxData,
        	tValidOut_o => toTxValid,
        	tReadyIn => toTxReady


	);

p_trig : process(clk_usr)
begin
	if rising_edge(clk_usr) then
		cnt3 <= cnt3+1;
		if cnt3 = 0 then
			trig <= '1';
		else
			trig <= '0';
		end if;
	end if;
end process;	



	
p_counter : process(clk_usr)
begin
	if rising_edge(clk_usr) then
		cnt <= cnt+1;
	end if;
end process;	


p_counter2 : process(clk_int)
begin
	if rising_edge(clk_int) then
		cnt2 <= cnt2+1;
	end if;
end process;

end Behavioral;


