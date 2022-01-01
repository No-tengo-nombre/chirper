import tkinter as tk
from tkinter import ttk
import time
import threading

from interface import GuiInterface


class MainWindow(tk.Frame):
    def __init__(self) -> None:
        super().__init__(self)
        self.pack()
        self.master_title("Chirper")
        self.button1 = tk.Button(self, text="")
        self.api = GuiInterface()


# class karl(tk.Frame):
#     def __init__(self):
#         tk.Frame.__init__(self)
#         self.pack()
#         self.master.title("Karlos")
#         self.button1 = tk.Button(self, text="CLICK HERE", width=25,
#                               command=self.new_window)
#         self.button1.grid(row=0, column=1, columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S)

#     def new_window(self):
#         self.newWindow = karl2()


# class karl2(tk.Frame):
#     def __init__(self):
#         new = tk.Frame.__init__(self)
#         new = tk.Toplevel(self)
#         new.title("karlos More Window")
#         new.button = tk.Button(text="PRESS TO CLOSE", width=25,
#                             command=self.close_window)
#         new.button.pack()

#     def close_window(self):
#         self.destroy()


def fix_dpi():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        pass


def center(root, w_width, w_height):
    s_width = root.winfo_screenwidth()
    s_height = root.winfo_screenheight()
    c_x = int(s_width / 2 - w_width / 2)
    c_y = int(s_height / 2 - w_height / 2)

    root.geometry(f"{w_width}x{w_height}+{c_x}+{c_y}")



class Root(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.loop = False
        self.var = 0

    def mainloop_alt(self):
        while self.loop:
            self.var += 1
            time.sleep(0.1)


def main():
    fix_dpi()
    root = Root()
    # root = tk.Tk()
    root.title("Chirper: Live signal analyzer")
    root.configure(bg="#111122")

    def loop_true():
        root.loop = True
        t = threading.Thread(target=root.mainloop_alt())
        t.start()


    def loop_false():
        root.loop = False

    # style = ttk.Style(root)
    # style.configure("Frame", bg="red")

    w_width = 1200
    w_height = 800
    center(root, w_width, w_height)

    message = ttk.Label(root, text=root.var)
    message.grid(row=0, column=0)

    btn = ttk.Button(root, text="Start", command=loop_true)
    btn.grid(row=0, column=1)

    message2 = tk.Label(root, text="Hello world!")
    message2.grid(row=1, column=0)

    btn2 = ttk.Button(root, text="Stop", command=loop_false)
    btn2.grid(row=1, column=1)

    root.mainloop()
    # root.mainloop_alt()


if __name__ == '__main__':
    main()
