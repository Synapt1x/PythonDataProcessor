'''
GUI - for Data Processor Project
============================
Created by: Chris Cadonic
For: Dr. Debbie Kelly lab
----------------------------
This program was developed to automatically
format input excel data for statistical
analysis in the statistical analysis
software.

IN:

OUT:

'''
import Tkinter # import Tkinter for gui
from PIL import Image, ImageTk
from Tkinter import Tk, Label, BOTH
from ttk import Frame, Style


root = Tkinter.Tk()  # create GUI root
root.wm_title('Data Processor')
root.geometry('360x240+300+300')
#root.wm_minsize(width=400,height=200)



class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()

    def toggle(toggle_btn):
        print toggle_btn.config('text')
        if toggle_btn.config('relief')[-1] == 'raised':
            toggle_btn.config(relief='sunken')
        else:
            toggle_btn.config(relief='raised')

    def initUI(self):

        self.parent.title("Data Processor")
        self.pack(fill=BOTH, expand=1)

        canvas = Tkinter.Canvas(self)
        canvas.create_line(0, 22, 360, 22)
        canvas.pack(fill=BOTH, expand=1)

        title_label = Tkinter.Label(root, text='Data Processor For Pigeon Experiment')
        title_label.place(x=60, y=5)

        #Style().configure("TFrame", background="#333")
        ctrl_button = Tkinter.Button(text='Control Group', width=12, relief='raised')
        ctrl_button.place(x=30, y=30)

        nr_button = Tkinter.Button(text='Non-reinforced', width=12, relief='raised')
        nr_button.place(x=30, y=65)

        bin_button = Tkinter.Button(text='Binocular', width=12, relief='raised')
        bin_button.place(x=30, y=100)

        capleft_button = Tkinter.Button(text='Cap-Left', width=12, relief='raised')
        capleft_button.place(x=30, y=135)

        capright_button = Tkinter.Button(text='Cap-Right', width=12, relief='raised')
        capright_button.place(x=30, y=170)

        threshold = Tkinter.Entry(root)
        threshold.insert(Tkinter.END, '50')
        threshold.pack()
        threshold.place(x=120, y=205)

        lab1 = Tkinter.Label(root, text='Threshold:')
        lab1.place(x=30, y=205)

        baby1_button = Tkinter.Button(text='Baby1', width=12, relief='raised', command=self.toggle)
        baby1_button.place(x=180, y=30)

        baby2_button = Tkinter.Button(text='Baby2', width=12, relief='sunken', command=self.toggle)
        baby2_button.place(x=180, y=65)

        baby3_button = Tkinter.Button(text='Baby3', width=12, relief='raised')
        baby3_button.place(x=180, y=100)



def main():
    app = App(root)
    root.mainloop()

if __name__ == '__main__':
    main()
