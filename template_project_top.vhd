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
library UNISIM;
use UNISIM.VComponents.all;

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
        serial1_rx : in STD_LOGIC; --Connected to db9


        phy_rxclk : in STD_LOGIC;
        phy_txclk : in STD_LOGIC;
        phy_txc_gtxclk : out STD_LOGIC;
        phy_reset : out STD_LOGIC;
        phy_mdio : inout STD_LOGIC;
        phy_mdc : out STD_LOGIC;
        phy_int : in STD_LOGIC
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

    signal rx_data : unsigned(7 downto 0);
    signal rx_data_valid : std_logic;
    signal rx_data_ready : std_logic;

    signal rxb_data : unsigned(7 downto 0);
    signal rxb_data_valid : std_logic;
    signal rxb_data_ready : std_logic;

    signal i_framed_data : unsigned(7 downto 0);
    signal i_framed_valid : std_logic;
    signal i_framed_ready : std_logic;
    signal i_framed_last : std_logic;

    signal o_framed_data : unsigned(7 downto 0);
    signal o_framed_valid : std_logic;
    signal o_framed_ready : std_logic;
    signal o_framed_last : std_logic;

    signal buf_data : unsigned(7 downto 0);
    signal buf_data_valid : std_logic;
    signal buf_data_ready : std_logic;

    signal tx_data : unsigned(7 downto 0);
    signal tx_data_valid : std_logic;
    signal tx_data_ready : std_logic;

    signal p0, p1, p2 : std_logic;
    signal cnt : unsigned(24 downto 0);
    signal clk_usr : std_logic;
    signal clk_int : std_logic;
    signal rst : std_logic;
    signal tx : std_logic;

    signal mdio_tristate : std_logic;
    signal phy_data_to_phy : std_logic;
    signal phy_data_from_phy : std_logic;
begin
    serial2_tx <= serial2_rx;
    serial1_tx <= tx;
    agreatb <= p0 or p1 or p2;
    p0 <= a(1) and (not b(1));
    p1 <= a(0) and (not b(1)) and (not b(0));
    p2 <= a(1) and a(0) and (not b(0));
    led_2 <= cnt(22);
    --hdr_2 <= serial1_rx;
    hdr_2 <= '0';
    hdr_4 <= '0';
    led_3 <= '1';
    led_4 <= rst;
    hdr_6 <= tx;
    rst <= not rst_in;



    phy_txc_gtxclk <= '0';
    phy_reset <= '0';
    --phy_mdio <= '0';
    --phy_mdc <= '0';

    --phy_data_to_phy <= '0';

    i_mdiobuf : IOBUF
    port map(
        t => mdio_tristate,
        io => phy_mdio,
        i => phy_data_to_phy,
        o => phy_data_from_phy
    );


    i_clk: clk
    port map (
        clkin_in => clk_in, 
            RST_IN => rst, 
            CLKIN_IBUFG_OUT=> clk_int, --(CLKIN_IBUFG_OUT), 
            CLKOUT0_OUT => clk_usr, 
            LOCKED_OUT => led_1
        );

    i_rs232rx: entity work.rs232rx 
        port map(
            reset => rst,
            clk => clk_usr,
            rxd => serial1_rx,
            baudDiv => to_unsigned(859, 24),
            o_data => rx_data,
            o_valid => rx_data_valid,
            o_ready => rx_data_ready
        );

    i_skid: entity work.axi4s_skidbuf
        port map(
            reset => rst,
            clk => clk_usr,
            i_data => rx_data,
            i_valid => rx_data_valid,
            i_ready => rx_data_ready,
            i_last => '0',
            o_data => rxb_data,
            o_valid => rxb_data_valid,
            o_ready => rxb_data_ready,
            o_last => open
        );

    i_axis_last_deescaper: entity work.axi4s_last_deescaper
        port map(
            reset => rst,
            clk => clk_usr,
            frameError => open,
            i_data => rxb_data,
            i_valid => rxb_data_valid,
            i_ready => rxb_data_ready,
            o_data => i_framed_data,
            o_valid => i_framed_valid,
            o_ready => i_framed_ready,
            o_last => i_framed_last
        );
    
    i_application_test_str: entity work.application_test_str
        port map(
            reset => rst,
            clk => clk_usr,
            i_data => i_framed_data,
            i_valid => i_framed_valid,
            i_ready => i_framed_ready,
            i_last => i_framed_last,
            o_data => o_framed_data,
            o_valid => o_framed_valid,
            o_ready => o_framed_ready,
            o_last => o_framed_last,

            mdio_in => phy_data_from_phy,
            mdio_out => phy_data_to_phy,
            mdio_tristate => mdio_tristate,
            mdio_clk => phy_mdc
        );       
    --o_framed_data <= i_framed_data;
    --o_framed_valid <= i_framed_valid;
    --i_framed_ready <= o_framed_ready;
    --o_framed_last <= i_framed_last;

    i_axis_last_escaper: entity work.axi4s_last_escaper
        port map(
            reset => rst,
            clk => clk_usr,
            i_data => o_framed_data,
            i_valid => o_framed_valid,
            i_ready => o_framed_ready,
            i_last => o_framed_last,
            o_data => buf_data,
            o_valid => buf_data_valid,
            o_ready => buf_data_ready
        );

    --buf_data <= i_framed_data;
    --buf_data_valid <= i_framed_valid;
    --i_framed_ready <= buf_data_ready;

    --buf_data <= rxb_data;
    --buf_data_valid <= rxb_data_valid;
    --rxb_data_ready <= buf_data_ready;

    i_fifo : entity work.axi4s_fifo
        port map(
            reset => rst,
            clk => clk_usr,
            i_data => buf_data,
            i_valid => buf_data_valid,
            i_ready => buf_data_ready,
            i_last => '0',
            o_data => tx_data,
            o_valid => tx_data_valid,
            o_ready => tx_data_ready,
            o_last => open
        );

    --tx_data <= rx_data;
    --tx_data_valid <= rx_data_valid;
    --rx_data_ready <= tx_data_ready;

    i_rs232tx: entity work.rs232tx 
        port map(
            reset => rst,
            clk => clk_usr,
            txd => tx,
            baudDiv => to_unsigned(859, 24),
            i_data => tx_data,
            i_valid => tx_data_valid,
            i_ready => tx_data_ready
        );



p_counter : process(clk_usr)
begin
    if rising_edge(clk_usr) then
        cnt <= cnt+1;
    end if;
end process;    


end Behavioral;


