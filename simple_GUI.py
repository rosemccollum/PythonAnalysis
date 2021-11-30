# Simple tkinter GUI- Created 04Nov2021, updated 15Nov2021

from tkinter import *

class graph_gui:
    def __init__ (self,root):
        # Setup GUI Window
        self.root = root
        root.title('Save Figure Name') # Set Window Name
        root.geometry('475x300') # Set Width vs. Height
        root.resizable(width=False,height=False) # Fix W/H

        # Add Labels
        self.label_1 = Label(root,text="Day of Recording (Ex: day1)").place(x=20,y=40)
        self.label_2 = Label(root,text="Animal Number (Ex: dev2107)").place(x=20,y=100)
        self.label_3 = Label(root, text = "File path (Ex: C:\TNE Lab\RatData)").place(x = 20, y = 150)
        self.label_4 = Label(root, text = "Choose the pre coherance data file first, then the post coherance data file").place(x=40, y =200)
        self.label_5 = Label(root, text = 'Used to select where figure is saved and name').place(x=20, y = 10)

        # Add Button
        self.btn = Button(root, text='Start Analysis',command=self.save_values).place(x=160,y=260)

        # Add and configure Entrys
        self.r_day = StringVar()
        self.a_num = StringVar()
        self.path = StringVar()
        self.entry_1 = Entry(root,width=20,textvariable=self.r_day).place(x=250,y=40)
        self.entry_2 = Entry(root,width=20,textvariable=self.a_num).place(x=250,y=100)
        self.entry_3 = Entry(root, width = 20, textvariable = self.path).place(x=250,y=150)

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
