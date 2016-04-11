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
#import Tkinter as tk# import tk for gui
from PIL import Image, ImageTk
from Tkinter import *
from ttk import Frame, Style
import tkFileDialog
import tkFont

root = Tk()  # create GUI root
root.wm_title('Data Processor') # create title label
root.geometry('480x360+300+300') # set the size of the window


class App(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.pack(fill=BOTH, expand=True)
        self.createComponents()
        #self.dataDirname = self.findDirectory()

    def findDirectory(self):
        while True:
            try:
                dataDirname = tkFileDialog.askdirectory(parent=self,
                    initialdir="/",title='Please select the data directory.')
                if not dataDirname:
                    raise ValueError('empty string')
                break
            except ValueError:
                print "Please select a valid directory..."
        return dataDirname

    def createComponents(self):
        # Create text fonts for components
        self.titleFont = tkFont.Font(family='Arial',size=18)
        self.componentFont = tkFont.Font(family='Helvetica',size=16)

        titleFrame = Frame(self)
        titleFrame.pack(fill=X)
        # Create the title label
        title_label = Label(titleFrame, text='Data Processor For Pigeon Experiment',
                            font=self.titleFont)
        title_label.pack(fill=X, expand=True)

        # Create a canvas for drawing a separation line
        canv = Canvas(titleFrame, width=480, height=10)
        canv.create_line(0, 10, 480, 10)
        canv.pack(fill=X, anchor=CENTER, expand=True)

        groupFrame = Frame(self)
        groupFrame.pack(fill=Y, expand=True, anchor=W, side=LEFT)
        # Create a checkbox for each test group
        grpLabels = ['Control Group','Non-reinforced','Binocular',
                       'Cap-Left','Cap-Right']
        for grpName in range(len(grpLabels)):
            grpButton = Checkbutton(groupFrame, text=grpLabels[grpName],
                                   variable=grpLabels[grpName],
                                   font=self.componentFont)
            grpButton.pack(pady=8)

        animalsFrame = Frame(self)
        animalsFrame.pack(fill=Y, expand=True, anchor=CENTER, side=LEFT)
        animals = ['Bird1','Bird2','Bird3',
                       'Bird4','Bird5']
        for bird in range(len(animals)):
            grpButton = Checkbutton(animalsFrame, text=animals[bird],
                                   variable=animals[bird],
                                   font=self.componentFont)
            grpButton.pack(pady=8)

        buttonsFrame = Frame(self)
        buttonsFrame.pack(fill=Y, expand=True, anchor=E)


        #footerFrame = Frame(self)
        #footerFrame.pack(fill=BOTH)
        # Create a quit button
        quitButton = Button(buttonsFrame, text='Quit', command=self.quit)
        quitButton.pack()

app = App(root) # place all components
root.mainloop()
