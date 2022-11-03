from pp_functions import Functions
from tkinter import *
from os import system
try:
    from pyperclip import copy
except ModuleNotFoundError:
    system('python -m pip install pyperclip')

buttons = [
    ['INV', 'π', 'e', '(', '←', 'C', '/', '//'],
    ['sin', 'cos', 'tan', '7', '8', '9', '*', '**'],
    ['log', 'ln', 'fact', '4', '5', '6', '+', '%'],
    ['pow', 'sqrt', 'abs', '1', '2', '3', False, '-'],
    ['ceil', 'floor', 'exp', '0', '00', '.', '=', False]
]

ops = '+ - * ** ^ / // %'.split()
nums = '12345678900'
funcs = 'asin sin acos cos atan tan fact log ln sqrt sqr abs ceil floor'.split()

inv_buttons = {
    'sin': 'asin', 'cos': 'acos', 'tan': 'atan',
    'log': '10^x', 'ln': 'e^x',
    'pow': 'root', 'sqrt': 'x^2'
}


class BackEnd(Functions):
    def __init__(self):
        Functions.__init__(self)
        self.allow_operator = False
        self.allow_constants = True
        self.allow_any = True

        self.angle_unit = StringVar()
        self.cursor = 0
        self.display_text = []
        self.textvar = StringVar()

    @staticmethod
    def is_num(n):
        if n.isdecimal() or (n.count('.') == 1 and n.replace('.', '').isdecimal()):
            return True
        return False

    @staticmethod
    def dec_to_e(n):
        b = int(n)
        if len(str(b)) > 1:
            c = n/(10**(len(str(b))-1))
            return f"{c}E{len(str(b))-1}"
        return n

    def count_ops(self, l):
        count = 0
        for i in l:
            if i in ops+funcs:
                count += 1
        return count

    def append_char_1c(self, *char):
        for i in char:
            a = len(self.display_text)
            self.display_text.insert(a+self.cursor, i)

    def clear_text(self):
        self.display_text.clear()
        self.allow_operator, self.allow_any, self.allow_constants = False, True, True
        self.cursor = 0

    def backspace_text(self):
        curr = len(self.display_text)+self.cursor-1
        if self.display_text[curr] == '(':
            self.display_text.pop(curr)
            self.cursor += 1
            self.backspace_text()
            if self.display_text and self.display_text[len(self.display_text)+self.cursor-1] in funcs:
                self.backspace_text()
        else:
            curr = len(self.display_text) + self.cursor - 1
            if self.is_num(self.display_text[curr]) and len(self.display_text[curr]) > 1:
                self.display_text[curr] = self.display_text[curr][:-1]
            else:
                self.display_text.pop(len(self.display_text)+self.cursor-1)

    def send_press(self, button):
        if button in ops+funcs and self.count_ops(self.display_text) > 14:
            return 0
        if button in funcs:
            if not self.allow_operator and self.allow_any:
                self.append_char_1c(button, '(', ')')
                self.cursor -= 1
        elif button == 'pow':
            if self.allow_operator:
                self.append_char_1c('^')
                self.allow_operator, self.allow_any, self.allow_constants = False, True, True
        elif button == 'exp':
            if self.allow_operator and self.display_text[len(self.display_text)+self.cursor-1]!='e':
                self.append_char_1c('E')
                self.allow_operator, self.allow_any, self.allow_constants = False, True, False
        elif button in ops:
            if self.allow_operator:
                if button == "**":
                    self.append_char_1c('^')
                else:
                    self.append_char_1c(button)
                self.allow_operator, self.allow_any, self.allow_constants = False, True, True
            else:
                if button == '-' and ((self.display_text and self.display_text[len(self.display_text)+self.cursor-1] != '-') or (not self.display_text)):
                    self.append_char_1c('-')
                    self.allow_operator, self.allow_any, self.allow_constants = False, True, True
        elif button in ('e', 'pi'):
            if self.allow_constants:
                if button == 'pi':
                    self.append_char_1c('π')
                else:
                    self.append_char_1c(button)
                self.allow_operator, self.allow_any, self.allow_constants = True, False, False
        elif button in nums:
            if self.allow_any:
                if not self.display_text:
                    self.append_char_1c(button)
                else:
                    if not self.is_num(self.display_text[len(self.display_text)+self.cursor-1]):
                        self.append_char_1c(button)
                    else:
                        self.display_text[len(self.display_text)+self.cursor-1] = self.display_text[len(self.display_text)+self.cursor-1] + str(button)
                self.allow_constants = False
                self.allow_operator = True
        elif button == 'C':
            self.clear_text()
        elif button == '=':
            print(self.display_text)
            self.deg_or_rad = self.angle_unit.get()
            b = self.eval_eq(self.textvar.get())
            self.display_text = [str(b)]
            if type(b) is str:
                self.allow_operator, self.allow_any, self.allow_constants = False, False, False
                self.cursor = 0
            else:
                if b >= 10**10000:
                    self.display_text = ['Overflow']
                    self.allow_any, self.allow_constants, self.allow_constants = False, False, False
                else:
                    if 10**45 <= b < 10**10000:
                        self.display_text = [str(self.dec_to_e(b))]
                    self.allow_operator, self.allow_any, self.allow_constants = True, False, False
                    self.cursor = 0
        elif button == '.':
            if self.display_text and self.display_text[len(self.display_text)+self.cursor-1].isdecimal():
                self.display_text[len(self.display_text)+self.cursor-1] += '.'
        elif button in ['10^x', 'e^x']:
            if not self.allow_operator and self.allow_any:
                self.append_char_1c(button.split('^')[0], '^')
                self.allow_operator, self.allow_any, self.allow_constants = False, True, True
        elif button == 'x^2':
            if self.allow_operator:
                self.append_char_1c('^', '2')
                self.allow_operator, self.allow_any, self.allow_constants = True, False, False
        elif button == '(':
            if not self.allow_operator and self.allow_any:
                self.append_char_1c('(', ')')
                self.cursor -= 1
                self.allow_operator, self.allow_any, self.allow_constants = False, True, True
        elif button == 'backspace':
            if self.display_text:
                self.backspace_text()
            curr = len(self.display_text)+self.cursor-1
            if not self.display_text:
                self.clear_text()
            elif self.is_num(self.display_text[curr]):
                self.allow_operator, self.allow_any, self.allow_constants = True, True, False
            elif self.display_text[curr] in ops+'(':
                self.allow_operator, self.allow_any, self.allow_constants = False, True, True
            elif self.display_text[curr] in 'πe':
                self.allow_operator, self.allow_any, self.allow_constants = True, False, False
        elif button == 'root':
            if self.allow_operator:
                self.append_char_1c('^', '(', '1', '/', ')')
                self.cursor -= 1
                self.allow_operator, self.allow_any, self.allow_constants = False, True, True
        else:
            self.append_char_1c(button)
            self.allow_operator = True

        self.textvar.set("".join(self.display_text))


class App(BackEnd):
    # colors
    light_grey = "#B8B8B8"
    dark_grey = "#535353"
    light_green = "#A3CDA8"
    dark_green = "#729177"
    orange = "#FFA662"
    dark_orange = "#C48542"

    def __init__(self, w: Tk):
        BackEnd.__init__(self)
        self.w = w
        self.meta_window()

        self.top_frame = Frame(self.w, bg=App.light_grey)
        self.bottom_frame = Frame(self.w, bg=App.dark_grey)
        self.place_mainframes()

        # top frame widgets
        self.tf_buttons = Frame(self.top_frame)
        self.tf_copy_button = Button(self.tf_buttons)
        self.tf_confirm_text = Label(self.tf_buttons)

        self.tf_textbox = Label(self.top_frame)

        self.tf_angle_selection_frame = Frame(self.top_frame)
        self.tf_asf_text = Label(self.tf_angle_selection_frame)
        self.tf_asf_rad_choice = Radiobutton(self.tf_angle_selection_frame)
        self.tf_asf_deg_choice = Radiobutton(self.tf_angle_selection_frame)

        self.place_tf_widgets()
        self.config_tf_widgets()

        # bottom frame widgets
        self.bf_buttons = []
        self.inverse_State = False
        self.place_bf_widgets()

    def meta_window(self):
        self.w.geometry("640x440")
        self.w.title("Project 16 - Scientific Calculator")
        self.w.config(bg=App.dark_grey)
        self.w.resizable(False, False)

        self.w.columnconfigure(0, weight=1)
        self.w.rowconfigure(1, weight=1)

    def place_mainframes(self):
        self.top_frame.grid(row=0, column=0, sticky=NSEW)
        self.top_frame.columnconfigure(0, weight=1)

        self.bottom_frame.grid(row=1, column=0, sticky=NSEW, padx=8, pady=8)
        self.bottom_frame.grid_propagate(False)
        for i in range(5):
            self.bottom_frame.rowconfigure(i, weight=1, uniform="xyz")
        for i in range(8):
            self.bottom_frame.columnconfigure(i, weight=1, uniform="xyz")

    def place_tf_widgets(self):
        self.tf_buttons.grid(row=0, column=0, pady=4, sticky=NSEW)
        self.tf_buttons.rowconfigure(0, weight=1)
        self.tf_buttons.grid_propagate(False)
        self.tf_copy_button.grid(row=0, column=0, padx=4, sticky=NSEW)

        self.tf_textbox.grid(row=1, column=0, sticky=NSEW, padx=4, pady=4)

        self.tf_angle_selection_frame.grid(row=2, column=0, sticky=W, pady=8, padx=4)
        self.tf_asf_text.grid(row=0, column=0, padx=4)
        self.tf_asf_rad_choice.grid(row=0, column=1, padx=16)
        self.tf_asf_deg_choice.grid(row=0, column=2, padx=4)

    def config_tf_widgets(self):
        self.tf_buttons.config(bg=App.light_grey, height=32)
        self.tf_copy_button.config(text="COPY", bg=App.dark_grey, activebackground=App.light_grey, fg="white", font=("Segoe UI", 13, 'bold'), borderwidth=3, command=lambda: copy_result())
        self.tf_confirm_text.config(text="Copied to Clipboard", bg=App.light_grey, fg="green", font=('Segoe UI', 10))
        self.tf_textbox.update()
        self.tf_textbox.config(
            height=2,
            font=("Courier New", 16, "bold"),
            textvariable=self.textvar,
            bg="white",
            borderwidth=2,
            relief=SOLID,
            wraplength=self.tf_textbox.winfo_width()-6,
            justify=RIGHT,
            anchor=NE
        )

        def toggle_angle():
            curr_ang = self.angle_unit.get()
            print(f"You selected {curr_ang}")
            if curr_ang == "deg":
                self.tf_asf_deg_choice.config(selectcolor="lime")
                self.tf_asf_rad_choice.config(selectcolor=App.light_grey)
            else:
                self.tf_asf_deg_choice.config(selectcolor=App.light_grey)
                self.tf_asf_rad_choice.config(selectcolor="lime")

        def copy_result():
            copy(self.textvar.get())
            self.tf_confirm_text.grid(row=0, column=1, padx=4, sticky=NSEW)
            self.tf_confirm_text.after(2000, lambda: self.tf_confirm_text.grid_remove())

        self.tf_angle_selection_frame.config(bg=App.light_grey)
        self.tf_asf_text.config(text="Angle: ", bg=App.light_grey, font=('Segoe UI', 14, 'normal'))
        self.tf_asf_rad_choice.config(text="Radians", selectcolor=App.light_grey, activebackground=App.light_grey, font=('Segoe UI', 14, 'normal'), variable=self.angle_unit, value="rad", command=toggle_angle, bg=App.light_grey)
        self.tf_asf_deg_choice.config(text="Degrees", selectcolor="lime", activebackground=App.light_grey, font=('Segoe UI', 14, 'normal'), variable=self.angle_unit, value="deg", command=toggle_angle, bg=App.light_grey)
        self.angle_unit.set("deg")

    def place_bf_widgets(self):
        for i in range(len(buttons)):
            row = []
            for j in range(len(buttons[i])):
                if buttons[i][j]:
                    b = Button(self.bottom_frame, text=buttons[i][j], bg=App.light_grey, borderwidth=3, font=('Segoe UI', 16, 'bold'), command=lambda x=buttons[i][j]: self.send_press(x))
                    if j > 2 or (i == 0 and 0 < j < 3):
                        b.config(font=('Segoe UI', 22, 'bold'))
                    row.append(b)
                    b.grid(row=i, column=j, sticky=NSEW, padx=4, pady=4)

            self.bf_buttons.append(row)

        self.bf_buttons[2][6].grid(row=2, column=6, rowspan=2)
        self.bf_buttons[4][6].grid(row=4, column=6, columnspan=2)
        self.bf_buttons[0][0].config(bg=App.light_green, activebackground=App.dark_green)
        self.bf_buttons[0][5].config(bg=App.orange, activebackground=App.dark_orange)
        self.bf_buttons[0][4].config(bg=App.orange, activebackground=App.dark_orange)
        self.bf_buttons[0][1].config(command=lambda f='pi': self.send_press(f))
        self.bf_buttons[0][4].config(command=lambda f='backspace': self.send_press(f))

        inv_rows = (1, 4)
        inv_cols = (0, 2)

        def inverse():
            if not self.inverse_State:
                for i in range(*inv_rows):
                    if i == 1:
                        self.bf_buttons[i][2].config(text=inv_buttons[buttons[i][2]], bg=App.light_green, command=lambda x=inv_buttons[buttons[i][2]]: [self.send_press(x), inverse()])
                    for j in range(*inv_cols):
                        self.bf_buttons[i][j].config(text=inv_buttons[buttons[i][j]], bg=App.light_green, command=lambda x=inv_buttons[buttons[i][j]]: [self.send_press(x), inverse()])
                self.bf_buttons[0][0].config(bg=App.dark_green, relief=SUNKEN)
                self.inverse_State = True
            else:
                for i in range(*inv_rows):
                    if i == 1:
                        self.bf_buttons[i][2].config(text=buttons[i][2], bg=App.light_grey, command=lambda x=buttons[i][2]: self.send_press(x))
                    for j in range(*inv_cols):
                        self.bf_buttons[i][j].config(text=buttons[i][j], bg=App.light_grey, command=lambda x=buttons[i][j]: self.send_press(x))
                self.bf_buttons[0][0].config(bg=App.light_green, relief=RAISED)
                self.inverse_State = False

        self.bf_buttons[0][0].config(command=lambda x=buttons[0][0]: [print(f"you pressed {x}"), inverse()])

    def start(self):
        self.w.mainloop()


if __name__ == '__main__':
    root = Tk()
    a = App(root)
    a.start()
