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
    Port ( a,b: in  STD_LOGIC_VECTOR (1 downto 0);
			  clk_in, rst_in : in std_logic;
           agreatb, led_1, led_2, led_3, led_4 : out  STD_LOGIC);
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

	signal p0, p1, p2 : std_logic;
	signal cnt : unsigned(24 downto 0);
	signal cnt2 : unsigned(24 downto 0);
	signal clk_usr : std_logic;
	signal clk_int : std_logic;
	signal rst : std_logic;
begin
	agreatb <= p0 or p1 or p2;
	p0 <= a(1) and (not b(1));
	p1 <= a(0) and (not b(1)) and (not b(0));
	p2 <= a(1) and a(0) and (not b(0));
	led_2 <= cnt(24);
	led_3 <= '1';
	led_4 <= cnt2(24);
	rst <= not rst_in;
	i_clk: clk
	port map (
	clkin_in => clk_in, 
    RST_IN => rst, 
    CLKIN_IBUFG_OUT=> clk_int, --(CLKIN_IBUFG_OUT), 
    CLKOUT0_OUT => clk_usr, 
    LOCKED_OUT => led_1
    );
	
	
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


