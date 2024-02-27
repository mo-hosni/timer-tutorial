from cocotb.triggers import ClockCycles, Edge, First, NextTimeStep
import cocotb
class SegmentsMonitor:
    def __init__(self, caravelEnv, digit_en_pins=[30, 29, 28, 27], digit_data_pins=[37, 36, 35, 34, 33, 32, 31]):
        self.digit_en_pins = digit_en_pins
        self.digit_data_pins = digit_data_pins
        self.caravelEnv = caravelEnv

    async def segment_change(self):
        # detect the changes at digit_en pins
        digit_en_edges = [Edge(self.caravelEnv.dut._id(f"gpio{digit_edge}_monitor", False)) for digit_edge in self.digit_en_pins]
        digit_data_edges = [Edge(self.caravelEnv.dut._id(f"gpio{digit_edge}_monitor", False)) for digit_edge in self.digit_data_pins]
        await First(*digit_en_edges, *digit_data_edges) # triggered with the first edge triggered
        digit_en = int(self.caravelEnv.monitor_discontinuous_gpios(self.digit_en_pins), 2)  # read digit_en pins
        digit = int(self.caravelEnv.monitor_discontinuous_gpios(self.digit_data_pins), 2)  # read digit pins
        if (digit_en == 0xE):
            digit_num = 0
        elif (digit_en == 0xD):
            digit_num = 1
        elif (digit_en == 0xB):
            digit_num = 2
        elif (digit_en == 0x7):
            digit_num = 3
        else:
            cocotb.log.error(f"[Test][read_seg] Invalid digit_en: {digit_en}")
        return digit_num, self.__int_to_seg(digit)

    def __int_to_seg(self, digit):
        return {
            0x7E: 0,
            0x30: 1,
            0x6D: 2,
            0x79: 3,
            0x33: 4,
            0x5B: 5,
            0x5F: 6,
            0x70: 7,
            0x7F: 8,
            0x7B: 9,
        }[digit]