import tkinter as tk
import cocotb
class GuiScreen:
    def __init__(self, title="7 segment display"):
        self.create_screen(title)
        self.initialze_screen()

    def create_screen(self, title, width=1500, height=500):
        cocotb.log.debug(f"[GUI_SCREEN][create_screen] title: {title}, width: {width}, height: {height}")
        self.root = tk.Tk()
        self.root.title(title)
        self.screen = tk.Canvas(self.root, width=width, height=height)
        self.screen.grid()
        self.dig3 = Digit(self.screen, 110, 110) 
        self.dig2 = Digit(self.screen, 360, 110) 
        TwoDots(self.screen, 610, 110, 710, 210) 
        TwoDots(self.screen, 610, 310, 710, 410)
        self.dig1 = Digit(self.screen, 804, 110)
        self.dig0 = Digit(self.screen, 1054, 110)

    def initialze_screen(self):
        cocotb.log.debug(f"[GUI_SCREEN][initialze_screen]")
        self.dig0.show(0)
        self.dig1.show(0)
        self.dig2.show(0)
        self.dig3.show(0)
        self.root.update()

    def update_digit(self, digit_num, digit):
        cocotb.log.debug(f"[GUI_SCREEN][update_digit] digit_num: {digit_num}, digit: {digit}")
        if digit > 9: 
            cocotb.log.error(f"[GUI_SCREEN][update_digit] Invalid digit: {digit} passed to update digit number {digit_num}")
        if (digit_num == 0):
            self.dig0.show(digit)
        elif (digit_num == 1):
            self.dig1.show(digit)
        elif (digit_num == 2):
            self.dig2.show(digit)
        elif (digit_num == 3):
            self.dig3.show(digit)
        self.root.update()


class Digit:
    def __init__(self, canvas, x=10, y=10, length=160, width=32):
        self.canvas = canvas
        l = length
        self.segs = []
        offsets = (
            (0, 0, 1, 0),  # top
            (1, 0, 1, 1),  # upper right
            (1, 1, 1, 2),  # lower right
            (0, 2, 1, 2),  # bottom
            (0, 1, 0, 2),  # lower left
            (0, 0, 0, 1),  # upper left
            (0, 1, 1, 1),  # middle
        )
        self.digits = (
            (1, 1, 1, 1, 1, 1, 0),  # 0
            (0, 1, 1, 0, 0, 0, 0),  # 1
            (1, 1, 0, 1, 1, 0, 1),  # 2
            (1, 1, 1, 1, 0, 0, 1),  # 3
            (0, 1, 1, 0, 0, 1, 1),  # 4
            (1, 0, 1, 1, 0, 1, 1),  # 5
            (1, 0, 1, 1, 1, 1, 1),  # 6
            (1, 1, 1, 0, 0, 0, 0),  # 7
            (1, 1, 1, 1, 1, 1, 1),  # 8
            (1, 1, 1, 1, 0, 1, 1),  # 9
            (0, 0, 0, 0, 0, 0, 0),  # disable
        )
        for x0, y0, x1, y1 in offsets:
            self.segs.append(canvas.create_line(
                x + x0*l, y + y0*l, x + x1*l, y + y1*l,
                width=width, state='normal'))

    def show(self, num):
        for iid, on in zip(self.segs, self.digits[num]):
            self.canvas.itemconfigure(iid, fill='#B90E0A' if on else "")

class TwoDots:
    def __init__(self, canvas, x=10, y=10, length=20, width=4):
        self.canvas = canvas
        canvas.create_oval(x, y, length, width, outline="#B90E0A" , fill="#B90E0A")