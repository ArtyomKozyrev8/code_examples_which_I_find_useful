import threading
import time
from tkinter import *
from tkinter import messagebox, filedialog, ttk

def do_work(_range, word, prbar):
    prbar.start()
    try:
        for i in range(_range):
            print(word)
            time.sleep(1)
            if i == 3:
                raise ValueError("Unona")
    except Exception as ex:
        messagebox.showerror("Error", str(ex))
    else:
        messagebox.showinfo("Info", message="Info message!!")
    finally:
        prbar.stop()

class MainForm(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("700x600")
        self.resizable(False, False)
        self.bt = Button(self, command=self.start_all, text="Start All", bd=5)
        self.prbar = ttk.Progressbar(self, orient=HORIZONTAL, length=300, mode='indeterminate')

    def grid_all(self):
            self.bt.grid(column=0, row=0, sticky=W, padx=20)
            self.prbar.grid(column=0, row=1, sticky=W, padx=20)

    def start_all(self):
            try:
                branch = threading.Thread(target=do_work, args=(10, "hello", self.prbar))
                branch.start()
            except Exception as ex:
                print(str(ex))
                messagebox.showerror("Error", message="Error message")

def main():
    app = MainForm()
    app.grid_all()
    app.mainloop()

if __name__ == "__main__":
    main()
