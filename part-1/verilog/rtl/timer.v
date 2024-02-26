/*
    A simple user's project example - Part 1
    Minutes and Seconds clock. The design drives 4 multiplexed 7-Segment display digits.
    It uses Caravel system clock and reset and 11 I/O pads. 
    The 11 I/O pads are divided between 4 digit enables and 7 segment drivers.
    The RTL supports:
     - Common Anode (CC=0) or Common Cathode (CC=1) multiplexed display
     - Different clock frequencies (FREQ in Hertz)
     - Different scans by sec (SCAN_PER_SEC)
*/

module timer #(parameter  CC = 1,
                                FREQ = 2_000,
                                SCAN_PER_SEC = 25) 
(
    input   wire        clk,
    input   wire        rst,
    output  wire [7:0]  seven_seg,
    output  wire [3:0]  digit_en     
);
    localparam DIG_DURATION = (FREQ)/(4 * SCAN_PER_SEC);

    // the counter
    reg [3:0]   sec_ones, sec_tens;
    reg [3:0]   min_ones, min_tens;
    wire        nine_sec        = (sec_ones == 4'd9);
    wire        fifty_nine_sec  = (sec_tens == 4'd5) & nine_sec;
    wire        nine_min        = (min_ones == 4'd9);
    wire        fifty_nine_min  = (min_tens == 4'd5) & nine_min;
    
    // Time Base Generators
    reg         sec;
    reg         scan;

    reg [31:0]  sec_div;
    reg [31:0]  scan_div;
    
    always @(posedge clk or posedge rst) begin
        if(rst)
            sec_div <= 32'b0;
        else if(sec_div == FREQ)
            sec_div <= 32'b0;
        else
            sec_div <= sec_div + 32'b1;
    end

    always @(posedge clk or posedge rst) begin
        if(rst)
            scan_div <= 32'b0;
        else if(scan_div == DIG_DURATION)
            scan_div <= 32'b0;
        else
            scan_div <= scan_div + 32'b1;
    end

    always @(posedge clk or posedge rst) begin
        if(rst)
            sec <= 1'b0;
        else if(sec_div == FREQ)
            sec <= 1'b1;
        else 
            sec <= 1'b0;
    end

    always @(posedge clk or posedge rst) begin
        if(rst)
            scan <= 1'b0;
        else if(scan_div == DIG_DURATION)
            scan <= 1'b1;
        else 
            scan <= 1'b0;
    end


    // Seconds Counters
    always @(posedge clk or posedge rst)
        if(rst) 
            sec_ones <=  4'b0;
        else if(sec) begin
            if(!nine_sec) 
                sec_ones <= sec_ones + 4'd1;
            else 
                sec_ones <= 0;
        end

    always @(posedge clk or posedge rst)
        if(rst) 
            sec_tens <=  4'b0;
        else if(sec) begin 
            if(fifty_nine_sec) 
                sec_tens <= 0;
            else if(nine_sec) 
                sec_tens <= sec_tens + 4'd1;
        end

    // Minutes Counters
    always @(posedge clk or posedge rst)
        if(rst) 
            min_ones <=  4'b0;
        else if(fifty_nine_sec & sec) begin
            if(!nine_min)
                min_ones <= min_ones + 4'd1;
            else
                min_ones <= 0;
        end

    always @(posedge clk or posedge rst)
        if(rst) 
            min_tens <=  4'b0;
        else if(fifty_nine_sec & sec) begin
            if(fifty_nine_min) 
                min_tens <= 0;
            else if(nine_min) 
                min_tens <= min_tens + 4'd1;
        end
    
    
        // Display TDM
        reg [1:0] dig_cnt;
        always @(posedge clk or posedge rst) begin
            if(rst)
                dig_cnt <= 2'b0;
            else
                if(scan) dig_cnt <= dig_cnt + 1'b1;
        end

        wire [3:0]  bcd_mux =   (dig_cnt == 2'b00) ? sec_ones :
                                (dig_cnt == 2'b01) ? sec_tens :
                                (dig_cnt == 2'b10) ? min_ones : min_tens;

        // BCD to 7SEG Decoder
        reg [7:0]   ca_7seg;
        wire[7:0]   cc_7seg = ~ ca_7seg;
        always @* begin
            ca_7seg = 7'b0000000;
            case(bcd_mux)
                4'd0 : ca_7seg = 7'b0000001;
                4'd1 : ca_7seg = 7'b1001111;
                4'd2 : ca_7seg = 7'b0010010;
                4'd3 : ca_7seg = 7'b0000110;
                4'd4 : ca_7seg = 7'b1001100;
                4'd5 : ca_7seg = 7'b0100100;
                4'd6 : ca_7seg = 7'b0100000;
                4'd7 : ca_7seg = 7'b0001111;
                4'd8 : ca_7seg = 7'b0000000;
                4'd9 : ca_7seg = 7'b0000100;
            endcase
        end

        generate
            if(CC==0) begin
                assign seven_seg    =   ca_7seg;
                assign digit_en     =   (4'b1 << dig_cnt);
            end else begin
                assign seven_seg    =   cc_7seg;
                assign digit_en     =   ~(4'b1 << dig_cnt);
            end
        endgenerate

endmodule