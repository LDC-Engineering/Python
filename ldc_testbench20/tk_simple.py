# importing whole module
from tkinter import *
from tkinter.ttk import *

# importing strftime function to
# retrieve system's time
import time
from time import strftime



class valueWindow():
    def __init__(self, label1_str='Freq:', label2_str='g+:', label3_str='g-:'):
        # creating tkinter window
        self.root = Tk()
        self.root.title('Data')
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.configure(background = 'purple')


        self.lbl = Label(self.root, font=('calibri', 40, 'bold'),
                    background='purple',
                    foreground='white')
     #   self.lbl.pack(anchor='center')
        self.lbl.grid(row=0, columnspan=2, sticky=W+E)
        self.lbl.config(text='TIME')


        # Styling the label widget so that clock
        # will look more attractive
        self.lbl1 = Label(self.root, font=('calibri', 40, 'bold'),
                    background='purple',
                    foreground='white')
        self.lbl1.grid(row=1, column=0, sticky=W)
        self.lbl1.config(text=label1_str)

        self.lbl2 = Label(self.root, font=('calibri', 40, 'bold'),
                    background='purple',
                    foreground='white')
        self.lbl2.grid(row=2, column=0, sticky=W)
        self.lbl2.config(text =label2_str)


        self.lbl3 = Label(self.root, font=('calibri', 40, 'bold'),
                    background='purple',
                    foreground='white')
        self.lbl3.grid(row=3, column=0, sticky=W)
        self.lbl3.config(text =label3_str)



        self.value1 = Label(self.root, font=('calibri', 40, 'bold'),
                    background='purple',
                    foreground='white')
        self.value1.grid(row=1, column=1, sticky=W)
        self.value1.config(text ='0.0')

        self.value2 = Label(self.root, font=('calibri', 40, 'bold'),
                    background='purple',
                    foreground='white')
        self.value2.grid(row=2, column=1, sticky=W)
        self.value2.config(text ='0.0')


        self.value3 = Label(self.root, font=('calibri', 40, 'bold'),
                    background='purple',
                    foreground='white')
        self.value3.grid(row=3, column=1, sticky=W)
        self.value3.config(text ='0.0')



    def update(self, value1='0.0', value2='0.0', value3='0.0'):
        self.time()
        self.value1.config(text=value1)
        self.value2.config(text=value2)
        self.value3.config(text=value3)
        self.root.update()
        self.root.update_idletasks()


    def time(self):
        string = strftime('%H:%M:%S %p')
        self.lbl.config(text=string)

    def close(self):
        self.root.destroy()







