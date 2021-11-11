# Tkinter demo - Created 04Nov2021, updated 11Nov2021

from tkinter import *

# Create the main, "root", window
root = Tk()

# Set Window Size
root.geometry('450x160') # Width vs. Height

# Add Labels
label_1 = Label(root,text="Day of Recording (Ex: day1)").place(x=20,y=20)
label_2 = Label(root,text="Animal Number (Ex: 2207)").place(x=20,y=60)

# Add Text
r_day = StringVar()
entry_1 = Entry(root,width=20,textvariable=r_day).place(x=220,y=20)
a_num = StringVar()
entry_2 = Entry(root,width=20,textvariable=a_num).place(x=220,y=60)

def save_values():
    rec_day = r_day.get()
    ani_num = a_num.get()
    print('Day: '+str(rec_day)+', Rat: '+str(ani_num))
    print('run '*3)

# Add Buttons
btn = Button(root, text='Start Analysis',command=save_values).place(x=160,y=110)

# Title the Popup
root.title('TNE Lab Coherence vs. Frequency Grapher')  # This is how you name the program window

# Lock Window Size
root.resizable(width=False, height=False)

# Run mainloop()
root.mainloop() # This tells the program to run and keep displaying