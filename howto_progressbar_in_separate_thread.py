# coding=cp866
import threading
import time
from tkinter import *
from tkinter import messagebox, filedialog, ttk


def do_work(_range, word, e, app):
    app.bt.config(state="disabled")
    separate_window = ProgressForm()
    separate_window.grid_all()
    app.protocol('WM_DELETE_WINDOW', app.stop_branch)
    try:
        for i in range(_range):
            print(word)
            time.sleep(1)
            if e.is_set():
                break
    except Exception as ex:
        separate_window.destroy()
        messagebox.showerror("Error", str(ex))
        app.protocol('WM_DELETE_WINDOW', app.destroy)
        app.bt.config(state="normal")
    else:
        if not e.is_set():
            separate_window.destroy()
            messagebox.showinfo("Info", message="Info message!!")
            app.protocol('WM_DELETE_WINDOW', app.destroy)
            app.bt.config(state="normal")


class ProgressForm(Toplevel):
    def __init__(self):
        super().__init__()
        self.resizable(False, False)
        self.protocol('WM_DELETE_WINDOW', self.do_nothing)
        self.geometry("260x100")
        self.title("Имя программы".upper())
        self.text = Label(self, text="Идет попытка обработки файла...")
        self.prbar = ttk.Progressbar(self, orient=HORIZONTAL, length=180, mode='indeterminate')

    def grid_all(self):
        self.text.grid(column=0, row=0, sticky=W, padx=20, pady=15)
        self.prbar.grid(column=0, row=1, sticky=W, padx=40)
        self.prbar.start()

    @staticmethod
    def do_nothing():
        pass

class MainForm(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x300")
        self.resizable(False, False)
        self.bt = Button(self, command=self.start_all, text="Start All", bd=5)
        self.event1 = threading.Event()

    def grid_all(self):
        self.bt.grid(column=0, row=0, sticky=W, padx=120, pady=130)

    def start_all(self):
        try:
            branch = threading.Thread(target=do_work, args=(10, "hello", self.event1, self),)
            branch.start()
        except Exception as ex:
            print(str(ex))
            messagebox.showerror("Error", message="Error message")

    def stop_branch(self):
        self.event1.set()
        time.sleep(3)
        self.destroy()


def main():
    app = MainForm()
    app.grid_all()
    app.mainloop()


if __name__ == "__main__":
    debug = False
    if not debug:
        main()
    else:
        try:
            main()
        except Exception as ex:
            print(str(ex))
            time.sleep(5)
