# Simple tkinter GUI- Created 04Nov2021, updated 15Nov2021

from tkinter import *

class graph_gui:
    def __init__ (self,root):
        # Setup GUI Window
        self.root = root
        root.title('TNE Lab Coherence vs. Frequency Grapher') # Set Window Name
        root.geometry('450x200') # Set Width vs. Height
        root.resizable(width=False,height=False) # Fix W/H

        # Add Labels
        self.label_1 = Label(root,text="Day of Recording (Ex: day1)").place(x=20,y=20)
        self.label_2 = Label(root,text="Animal Number (Ex: dev2107)").place(x=20,y=60)
        self.label_3 = Label(root, text = "File path (Ex: C:\TNE Lab\RatData)").place(x = 20, y = 100)

        # Add Button
        self.btn = Button(root, text='Start Analysis',command=self.save_values).place(x=160,y=160)

        # Add and configure Entrys
        self.r_day = StringVar()
        self.a_num = StringVar()
        self.path = StringVar()
        self.entry_1 = Entry(root,width=20,textvariable=self.r_day).place(x=220,y=20)
        self.entry_2 = Entry(root,width=20,textvariable=self.a_num).place(x=220,y=60)
        self.entry_3 = Entry(root, width = 20, textvariable = self.path).place(x = 220, y = 100)

    def save_values(self):
        global rec_day
        global ani_num
        global path_name
        rec_day = self.r_day.get()
        ani_num = self.a_num.get()
        path_name = self.path.get()
        print('Analyzing - Day: ' + str(rec_day) + ', Rat: ' + str(ani_num))  
        self.root.destroy()

root = Tk()
tnel_gui = graph_gui(root)
root.mainloop()
