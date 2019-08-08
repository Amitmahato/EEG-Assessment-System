import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from multiprocessing import Process, Manager, Queue
from queue import Empty
from threading import Thread
from tkinter.messagebox import *

import sys
import os
# sys.path.append(os.path.abspath('../'))  #to import files from sibling directory

from uploadpage import FILESPATH, Upload
# from processpage import Processing
from resultpage import Results
from Abstraction import Abstraction

class StartPage(tk.Frame):
    def __init__(self,parent,controller,*args):
        tk.Frame.__init__(self,parent,bg='white')
        self.controller = controller


        ###     file structure    ###
        ###     file structure    ###
        fileHierarchyFrame = tk.Frame(self,width=210,height=450,bg="lightgray",padx=10,pady=10,highlightthickness=1,relief="solid",highlightbackground="gray")
        self.fileStructure = ttk.Treeview(fileHierarchyFrame)
        self.fileStructure.config(height=17)
        self.fileStructure.heading('#0',text='EDF Files')
        self.fileStructure.bind("<Double-1>", self.OnDoubleClick)
        self.fileStructure.grid(row=0,column=0,sticky='news')
        self.fileStructure.tk_focusPrev()
        self.fileStructure.column("#0",width=1,anchor="center")
        
        spacing = tk.Label(fileHierarchyFrame,height=1)
        spacing.config(bg="lightgray")
        spacing.grid(row=1,column=0)

        self.addnew = tk.Button(fileHierarchyFrame,text='Add New File', font=("Arial", "10", "bold"),command=lambda:controller.showFrame(Upload))
        self.addnew.configure(padx=50,pady=2)
        self.addnew.grid(row=2,column=0)
        self.addnew.focus()

        spacing = tk.Label(fileHierarchyFrame,height=10)
        spacing.config(bg="lightgray")
        spacing.grid(row=3,column=0)
        
        fileHierarchyFrame.grid(row=0,column=0)
        fileHierarchyFrame.grid_propagate(False)

        tk.Label(self,width=1,bg="white").grid(row=0,column=1)

        ###     patient details    ###
        ###     patient details    ###
        self.detailFrame = tk.Frame(self,width=550,height=450,bg='white smoke',padx=10,pady=10,bd=4)
        detailFont = tkFont.Font(family="Times", size="14")

        #before uploading any file
        self.uploadFrame = tk.Frame(self.detailFrame,bg='white smoke',width=550,height=450)
        tk.Label(self.uploadFrame,bg='white smoke',text='Welcome to EEG Assessment Application',font=("Arial","16","bold")).place(relx=0.45,rely=0.3,anchor="center")
        tk.Label(self.uploadFrame,bg='white smoke',text='<----- Please upload some files there',font=("Arial","12")).place(relx=0.425,rely=0.5,anchor="center")
        self.uploadFrame.grid(row=0,column=0)
        
        #before selection of any file
        self.selectFrame = tk.Frame(self.detailFrame,bg='white smoke',width=550,height=450)
        tk.Label(self.selectFrame,bg='white smoke',text='Welcome to EEG Assessment Application',font=("Arial","16","bold")).place(relx=0.45,rely=0.3,anchor="center")
        tk.Label(self.selectFrame,bg='white smoke',text='<----- Please select a file for information & analysis',font=("Arial","12")).place(relx=0.425,rely=0.5,anchor="center")
        self.selectFrame.grid(row=0,column=0)

        #after selection of a file
        self.infoFrame = tk.Frame(self.detailFrame,bg='white smoke',width=550,height=450)
        self.infoFrame.rowconfigure(0,pad=50)
        tk.Label(self.infoFrame,bg='white smoke').grid(row=0,column=1,sticky="ews")
        tk.Label(self.infoFrame,bg='white smoke',text='Basic Information',font=("Times", "24", "bold")).place(relx=0.45,rely=0.05,anchor="center")
        
        tk.Label(self.infoFrame,bg='white smoke',text='Patient Name',font=detailFont).grid(row=1,column=0,sticky="new")
        tk.Label(self.infoFrame,bg='white smoke',text='Doctor Name',font=detailFont).grid(row=2,column=0,sticky="new")
        tk.Label(self.infoFrame,bg='white smoke',text='Diagonosis Date',font=detailFont).grid(row=3,column=0,sticky="new")
        tk.Label(self.infoFrame,bg='white smoke',text='Diagonosis Time',font=detailFont).grid(row=4,column=0,sticky="new")
        
        tk.Label(self.infoFrame,bg='white smoke',text=':',font=detailFont).grid(row=1,column=1)
        tk.Label(self.infoFrame,bg='white smoke',text=':',font=detailFont).grid(row=2,column=1)
        tk.Label(self.infoFrame,bg='white smoke',text=':',font=detailFont).grid(row=3,column=1)
        tk.Label(self.infoFrame,bg='white smoke',text=':',font=detailFont).grid(row=4,column=1)
        
        self.p_name = tk.Label(self.infoFrame,bg='white smoke',text='',font=detailFont)
        self.p_name.grid(row=1,column=2,columnspan=2,sticky="w")
        self.d_name = tk.Label(self.infoFrame,bg='white smoke',text='',font=detailFont)
        self.d_name.grid(row=2,column=2,columnspan=2,sticky="w")
        self.d_date = tk.Label(self.infoFrame,bg='white smoke',text='',font=detailFont)
        self.d_date.grid(row=3,column=2,columnspan=2,sticky="w")
        self.d_time = tk.Label(self.infoFrame,bg='white smoke',text='',font=detailFont)
        self.d_time.grid(row=4,column=2,columnspan=2,sticky="w")

        tk.Label(self.infoFrame,bg='white smoke',width=10,height=12).grid(row=5,column=0)
        tk.Label(self.infoFrame,bg='white smoke',width=10,height=0).grid(row=6,column=0)

        self.pgbar = ttk.Progressbar(self.infoFrame, length=100, mode='indeterminate')
        self.pgbar.grid(row=7,column=0,columnspan=2,sticky="news")
        self.analyse = tk.Button(self.infoFrame,text="Analyse",width=24, font=("Arial", "10", "bold"),relief="raised", command=lambda:self.Analyse())
        self.analyse.grid(row=7,column=2,sticky="news",padx=10)
        
        self.infoFrame.grid_remove()
        self.infoFrame.columnconfigure(1,pad=150)
        self.infoFrame.grid_propagate("False")

        self.uploadFrame.tkraise()
        self.detailFrame.grid(row=0,column=2)
        self.detailFrame.grid_propagate("False")

    def insertIntoHierarchy(self,parent='top',filePath=''):
        if len(self.fileStructure.get_children()) == 0:
            self.uploadFrame.grid_remove()
            self.selectFrame.grid(row=0,column=0)

        text = str(filePath.split('/')[-1])
        self.fileStructure.insert(parent,index='end',iid=text,text=text,values=filePath)

    def moveItems(self,moveitem,into='top'):
        self.fileStructure.move(moveitem,into,index='end')
    
    def OnDoubleClick(self, event):
        item = self.fileStructure.selection()[0]
        value = self.fileStructure.item(item)['values']
        self.selectedFilePath = ''.join(value)
        ptFilePath = self.selectedFilePath.split('/')[-1]
        try:
            p_info = self.getDetails(ptFilePath)
            self.p_name['text'] = p_info[1]
            self.d_name['text'] = p_info[2]
            self.d_date['text'] = p_info[3]
            self.d_time['text'] = p_info[4]
        except:
            self.p_name['text'] = ''
            self.d_name['text'] = ''
            self.d_date['text'] = ''
            self.d_time['text'] = ''
            showwarning("No Information","The selected file doesn't contain any patient related information")
        
        self.selectFrame.grid_remove()
        self.infoFrame.grid(row=0,column=0)
    
    def getDetails(self,filename):
        print(filename)
        filename_modified = "data/Cheats/"+filename[-9:-4]+"/ptFile.dat"
        print(filename_modified)
        patient = open(filename_modified,'rb')
        patient.read(25)
        pt_details = []
        s = patient.read(1)
        for i in range(5):
            while ord(s)==32:
                s = patient.read(1)
                continue
            level = 0
            pt_name = ''
            count = 0
            while level<2:
                if ord(s)!=32:
                    level = 0
                else:
                    level+=1
                pt_name+= chr(ord(s))
                count+=1
                s= patient.read(1)
            pt_details.append(pt_name)
        pt_details[3] = pt_details[3].split()[0][:-2]
        ind = pt_details[4].index(':')
        pt_details[4] = pt_details[4][ind-2:ind+6]
        patient.close()
        return pt_details

    def Analyse(self):
        #using fullpath
        self.pgbar.start(10)
        self.analyse.config(state="disabled")
        self.addnew.config(state="disabled")
        tempFilePath = self.selectedFilePath.split("/")
        tempFilePath = '\\'.join(tempFilePath)

        self.processData = Abstraction(tempFilePath)
        self.p1 = Thread(target = self.compute)
        self.p1.start()
        self.pgbar.start(10)
        self.after(100,self.onProcessComplete)
    
    def compute(self):
        self.processData.run()

    def onProcessComplete(self):
        if (self.p1.is_alive()):
            self.after(100, self.onProcessComplete)
            return
        else:    
           try:
                self.pgbar.stop()
                self.analyse.config(state="normal")
                self.addnew.config(state="normal")
                self.controller.showFrame(Results,self.processData)
           except Empty:
                showerror("Empty","Queue is empty")