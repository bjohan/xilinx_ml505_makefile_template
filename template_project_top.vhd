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
        clk_fpga_p : in std_logic;
        clk_fpga_n : in std_logic;
        agreatb, led_1, led_2, led_3, led_4 : out  STD_LOGIC;
        hdr_2 : out STD_LOGIC;
        hdr_4 : out STD_LOGIC;
        hdr_6 : out STD_LOGIC;
        serial2_tx : out STD_LOGIC;
        serial2_rx : in STD_LOGIC;
        serial1_tx : out STD_LOGIC; --Connected to db9
        serial1_rx : in STD_LOGIC; --Connected to db9


        phy_reset : out STD_LOGIC;
        phy_mdio : inout STD_LOGIC;
        phy_mdc : out STD_LOGIC;
        phy_int : in STD_LOGIC;

        phy_crs : in std_logic;
        phy_col : in std_logic;
        phy_rxclk : in std_logic;
        phy_rxer : in std_logic;
        phy_rxctl_rxdv : in std_logic;
        phy_rxd : in STD_LOGIC_VECTOR(7 downto 0);
        phy_txc_gtxclk : out std_logic;
        phy_txclk : in std_logic;
        phy_txer : out std_logic;
        phy_txctl_txen : out std_logic;
        phy_txd : out STD_LOGIC_VECTOR(7 downto 0)
        --sgmii_rx_p : in std_logic;
        --sgmii_rx_n : in std_logic;
        --sgmii_tx_p : out std_logic;
        --sgmii_tx_n : out std_logic
);
end template_project_top;

architecture Behavioral of template_project_top is

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
    signal clk_usr2 : std_logic;
    signal clk_usr : std_logic;
    signal clk_int : std_logic;
    --signal clk_fpga : std_logic;
    signal rst : std_logic;
    signal tx : std_logic;

    signal mdio_tristate : std_logic;
    signal phy_data_to_phy : std_logic;
    signal phy_data_from_phy : std_logic;
    signal clk_enet : std_logic;
    signal locked_clk_enet : std_logic;

    signal debug0 : unsigned(15 downto 0);

    signal cdc_in : std_logic_vector(11 downto 0);
    signal cdc_out : std_logic_vector(11 downto 0);
    signal cdc_empty : std_logic;
begin
    serial2_tx <= serial2_rx;
    serial1_tx <= tx;
    agreatb <= p0 or p1 or p2;
    p0 <= a(1) and (not b(1));
    p1 <= a(0) and (not b(1)) and (not b(0));
    p2 <= a(1) and a(0) and (not b(0));
    led_2 <= cnt(22);
    hdr_2 <= serial1_rx;
    --hdr_2 <= phy_rxclk;
    hdr_4 <= clk_enet;
    led_3 <= locked_clk_enet;
    led_4 <= rst;
    hdr_6 <= tx;
    rst <= not rst_in;


    phy_txc_gtxclk <= clk_enet;
    phy_reset <= '1'; --inverted
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

    --i_ibufds : IBUFDS
    --port map(
    --    i => clk_fpga_p,
    --    ib => clk_fpga_n,
    --    o => clk_fpga
    --);

    i_clk: entity work.clk
    port map (
        clkin_in => clk_in, 
            RST_IN => rst, 
            CLKIN_IBUFG_OUT=> clk_int, --(CLKIN_IBUFG_OUT), 
            CLKOUT0_OUT => clk_usr2, 
            LOCKED_OUT => led_1
        );

    i_clk_125_enet : entity work.clk_125_enet
    port map(
        clkin1_p_in => clk_fpga_p,
        clkin1_n_in => clk_fpga_n,
        rst_in => rst,
        clkout0_out => clk_enet,
        locked_out => locked_clk_enet
    );
    clk_usr <= clk_enet;
    i_rs232rx: entity work.rs232rx 
        port map(
            reset => rst,
            clk => clk_usr,
            rxdi => serial1_rx,
            --baudDiv => to_unsigned(859, 24),
            baudDiv => to_unsigned(1085, 24),
            o_data => rx_data,
            o_valid => rx_data_valid,
            o_ready => rx_data_ready
        );

    --i_skid: entity work.axi4s_skidbuf
    --    port map(
    --        reset => rst,
    --        clk => clk_usr,
    --        i_data => rx_data,
    --        i_valid => rx_data_valid,
    --        i_ready => rx_data_ready,
    --        i_last => '0',
    --        o_data => rxb_data,
    --        o_valid => rxb_data_valid,
    --        o_ready => rxb_data_ready,
    --        o_last => open
    --    );

    i_axis_last_deescaper: entity work.axi4s_last_deescaper
        port map(
            reset => rst,
            clk => clk_usr,
            frameError => open,
            i_data => rx_data,
            i_valid => rx_data_valid,
            i_ready => rx_data_ready,
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
            mdio_out_o => phy_data_to_phy,
            mdio_tristate_o => mdio_tristate,
            mdio_clk_o => phy_mdc,

            debug0 => debug0
        );
       
    --phy_data_to_phy <= '0';
    --phy_mdc <= '0';
    --mdio_tristate <= '1';
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

    --i_fifo : entity work.axi4s_fifo
    --    port map(
    --        reset => rst,
    --        clk => clk_usr,
    --        i_data => buf_data,
    --        i_valid => buf_data_valid,
    --        i_ready => buf_data_ready,
    --        i_last => '0',
    --        o_data => tx_data,
    --        o_valid => tx_data_valid,
    --        o_ready => tx_data_ready,
    --        o_last => open
    --    );


    tx_data <=buf_data;
    tx_data_valid <= buf_data_valid;
    buf_data_ready <= tx_data_ready;
    --tx_data <= rx_data;
    --tx_data_valid <= rx_data_valid;
    --rx_data_ready <= tx_data_ready;

    i_rs232tx: entity work.rs232tx 
        port map(
            reset => rst,
            clk => clk_usr,
            txd => tx,
            --baudDiv => to_unsigned(859, 24),
            baudDiv => to_unsigned(1085, 24),
            i_data => tx_data,
            i_valid => tx_data_valid,
            i_ready => tx_data_ready
            --i_data => rx_data,
            --i_valid => rx_data_valid,
            --i_ready => rx_data_ready
        );
    --tx <= serial1_rx;

    i_cdc_fifo : entity work.cdc_fifo
    port map (
        rst => rst,
        wr_clk => phy_rxclk,
        rd_clk => clk_usr,
        din => cdc_in,
        wr_en => '1',
        rd_en => '1',
        dout => cdc_out,
        full => open,
        empty => cdc_empty
    );

    cdc_in(7 downto 0) <= phy_rxd;
    
    cdc_in(8) <= phy_rxctl_rxdv;
    cdc_in(9) <= phy_rxer;
    cdc_in(10) <= phy_col;
    cdc_in(11) <= phy_crs;

    phy_txd <= cdc_out(7 downto 0);
    phy_txctl_txen <= cdc_out(8);
    phy_txer <= cdc_out(9);

    --phy_txd <= phy_rxd;
    --phy_txctl_txen <= phy_rxctl_rxdv;
    --phy_txer <= phy_rxer;

    debug0(0) <= cdc_out(8); --dv
    debug0(1) <= cdc_out(9); --er
    debug0(2) <= cdc_out(10); --col
    debug0(3) <= cdc_out(11); --crs
    debug0(7 downto 4) <= "0000";
    debug0(8) <= cdc_out(7);
    debug0(9) <= cdc_out(6);
    debug0(10) <= cdc_out(5);
    debug0(11) <= cdc_out(4);
    debug0(12) <= cdc_out(3);
    debug0(13) <= cdc_out(2);
    debug0(14) <= cdc_out(1);
    debug0(15) <= cdc_out(0);
    --debug0(0) <= cdc_out(8);
    --debug0(8 downto 1) <= unsigned(phy_rxd);
    --debug0(8 downto 1) <= unsigned(cdc_out(7 downto 0));
    --debug0(9) <= phy_rxer;
    --debug0(9) <= cdc_out(9);
    --debug0(10) <= phy_rxclk;
    --debug0(11) <= phy_txclk;
    --debug0(15 downto 10) <= "000000";
    --debug0(15 downto 0) <= "0000000000000000";
    --debug0(15 downto 0) <= "1111111111111111";
    --debug0(15 downto 12) <= "0000";

p_counter : process(clk_usr)
begin
    if rising_edge(clk_usr) then
        cnt <= cnt+1;
    end if;
end process;    


end Behavioral;


