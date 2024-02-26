from caravel_cocotb.caravel_interfaces import report_test
import cocotb
from caravel_cocotb.caravel_interfaces import test_configure
from gui_screen import GuiScreen
from segments_monitor import SegmentsMonitor


@cocotb.test()
# use report_test for configuring the logs correctly
@report_test
async def seven_seg(dut):
    # initialize the display gui before powering caravel on
    screen = GuiScreen()
    # configure file used for configuring caravel power, clock, and reset and setup the timeout watchdog then return object of caravel environment.
    caravelEnv = await test_configure(dut, timeout_cycles=275837)
    # initialize the monitor over the segments
    segements_monitor = SegmentsMonitor(caravelEnv)
    while True:
        # forever loop that detects any change at digit the update the display
        digit_num, digit = await segements_monitor.segment_change()
        screen.update_digit(digit_num, digit)
