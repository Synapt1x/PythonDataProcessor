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

    def allButtons(self,buttonGroup, event):
        for buttonNum in range(len(buttonGroup)):
            if event == 'Select':
                buttonGroup[buttonNum].set(1)
            else:
                buttonGroup[buttonNum].set(0)

    def createComponents(self):
        # Create text fonts for components
        self.titleFont = tkFont.Font(family='Arial',size=18)
        self.componentFont = tkFont.Font(family='Helvetica',size=16)

        # Create a frame for the title section
        #======================================================================
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


        # Create a frame for the group buttons
        #======================================================================
        grpFrame = Frame(self)
        grpFrame.pack(fill=Y, expand=True, anchor=W, side=LEFT)
        # Create a checkbox for each test group
        grpLabels = ['Control Group','Non-reinforced','Binocular',
                       'Cap-Left','Cap-Right']
        grpVals = []
        grpButtons = []
        # Create all of the group buttons
        for grpName in range(len(grpLabels)):
            grpVals.append(IntVar())
            grpButtons.append(Checkbutton(grpFrame, text=grpLabels[grpName],
                                   variable=grpVals[grpName],
                                   font=self.componentFont))
            grpButtons[-1].pack(pady=8)
        grpCanv = Canvas(grpFrame, width=220, height=10)
        grpCanv.create_line(20,10,220,10, dash=(2,4))
        grpCanv.pack(fill=X)

        # Add some select / de-select all buttons
        selectAllGrps = Button(grpFrame, text='Select All',
                         command=lambda:
                         self.allButtons(grpVals,'Select')).pack()
        deselectAllGrps = Button(grpFrame, text='De-Select All',
                           command=lambda:
                           self.allButtons(grpVals,'De-Select')).pack()


        # Create a frame for handling all of the birds
        #======================================================================
        animalsFrame = Frame(self)
        animalsFrame.pack(fill=Y, expand=True, anchor=CENTER, side=LEFT)
        animals = ['Bird1','Bird2','Bird3',
                       'Bird4','Bird5']
        animalVals = []
        animalButtons = []
        # Create a button for each bird in the data directory
        for bird in range(len(animals)):
            animalVals.append(IntVar())
            animalButtons.append(Checkbutton(animalsFrame, text=animals[bird],
                                   variable=animalVals[bird],
                                   font=self.componentFont))
            animalButtons[-1].pack(pady=8)
        animalsCanv = Canvas(animalsFrame, width=220, height=10)
        animalsCanv.create_line(20,10,220,10, dash=(2,4))
        animalsCanv.pack(fill=X)

        # Add some select / de-select all buttons
        selectAllAnimals = Button(animalsFrame, text='Select All',
                         command=lambda:
                         self.allButtons(animalVals,'Select')).pack()
        deselectAllAnimals = Button(animalsFrame, text='De-Select All',
                           command=lambda:
                           self.allButtons(animalVals,'De-Select')).pack()


        # Create a frame for handling all of the additional buttons
        #======================================================================
        buttonsFrame = Frame(self)
        buttonsFrame.pack(fill=Y, expand=True, anchor=E)

        # Create a quit button
        quitButton = Button(buttonsFrame, text='Quit', command=self.quit)
        quitButton.pack(fill=X)


        # Create a frame for the bottom section
        #======================================================================
        footerFrame = Frame(self)
        footerFrame.pack(anchor=CENTER, expand=True)

        '''bottomCanv = Canvas(footerFrame, width=480, height=10)
        bottomCanv.create_line(0,5,480,5)
        bottomCanv.pack(fill=Y,expand=True)'''

app = App(root) # place all components
root.mainloop() # run the GUI
