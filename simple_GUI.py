# Tkinter demo - Created 04Nov2021, updated 12Nov2021

from tkinter import *

class graph_gui:
    def __init__ (self,root):
        # Setup GUI Window
        self.root = root
        root.title('TNE Lab Coherence vs. Frequency Grapher') # Set Window Name
        root.geometry('450x160') # Set Width vs. Height
        root.resizable(width=False,height=False) # Fix W/H

        # Add Labels
        self.label_1 = Label(root,text="Day of Recording (Ex: day1)").place(x=20,y=20)
        self.label_2 = Label(root,text="Animal Number (Ex: 2207)").place(x=20,y=60)

        # Add Button
        self.btn = Button(root, text='Start Analysis',command=self.save_values).place(x=160,y=110)

        # Add and configure Entrys
        self.r_day = StringVar()
        self.a_num = StringVar()
        self.entry_1 = Entry(root,width=20,textvariable=self.r_day).place(x=220,y=20)
        self.entry_2 = Entry(root,width=20,textvariable=self.a_num).place(x=220,y=60)

    def save_values(self):
        rec_day = self.r_day.get()
        ani_num = self.a_num.get()
        print('Day: '+str(rec_day)+', Rat: '+str(ani_num))

root = Tk()
tnel_gui = graph_gui(root)
root.mainloop()
