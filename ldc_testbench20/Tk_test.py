# importing whole module
from tkinter import *
from tkinter.ttk import *

# importing strftime function to
# retrieve system's time
import time
from time import strftime



class valueWindow():
    def __init__(self):
        # creating tkinter window
        self.root = Tk()
        self.root.title('Clock')

        # Styling the label widget so that clock
        # will look more attractive
        self.lbl = Label(self.root, font=('calibri', 40, 'bold'),
                    background='purple',
                    foreground='white')

        # Placing clock at the centre
        # of the tkinter window
        self.lbl.pack(anchor='center')

        self.f_lbl = Label(self.root, font=('calibri', 40, 'bold'),
                    background='purple',
                    foreground='white')

        self.f_lbl.pack(anchor='center')
        self.f_lbl.config(text ='hello')

    def update(self):
        self.time()
        self.fill_strings("test")
        self.root.update()
        self.root.update_idletasks()


    def time(self):
        string = strftime('%H:%M:%S %p')
        self.lbl.config(text=string)

    def fill_strings(self, freq_str = ''):
        self.f_lbl.config(text = freq_str)





x = valueWindow()

while(True):
    time.sleep(1)
    x.update();

