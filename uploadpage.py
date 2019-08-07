import tkinter as tk
from tkinter import filedialog, messagebox, ttk

FILESPATH = ['']

class Upload(tk.Frame):
    def __init__(self,parent,controller,*args):
        tk.Frame.__init__(self,parent)
        
        #logo
        imgFrame = tk.Frame(self)
        tk.Label(imgFrame,width=18).grid(row=0,column=0)
        self.__logoimg = tk.PhotoImage(file="./static/logo1_1.png")
        self.__logoLabel = tk.Label(imgFrame, anchor=tk.CENTER, image=self.__logoimg,height=300)
        self.__logoLabel.grid(row=0,column=2,sticky="news")
        # self.__logoLabel.place(relx=0.5, y=150, anchor=tk.CENTER)
        imgFrame.grid(row=0,column=0,columnspan=5,sticky="news")
        
        #gap between logo and filepath entry and browse button
        tk.Label(self,height=5).grid(row=1,column=0,rowspan=2)

        #the filepath entry and browse side by side
        fileFrame = tk.Frame(self)
        tk.Label(fileFrame,width=15).grid(row=0,column=0)
        self.filePath = tk.StringVar()
        filePathEntry = tk.Entry(fileFrame,textvariable=self.filePath,width=65, font=("Arial", "10", ""))
        filePathEntry.grid(row = 0,column=1,sticky="news")

        browseBtn = tk.Button(fileFrame,text="Browse", font=("Arial", "10", "bold"),command=self.getFileName)
        browseBtn.grid(row = 0,column=3,sticky="news",padx=20)
        browseBtn.focus()
        fileFrame.grid(row=2,column=0,sticky="news")

        #for gap between fileframe and next button
        tk.Label(self).grid(row=3,column=0)

        #the next button
        buttonFrame = tk.Frame(self)
        #for spacing from left side
        tk.Label(buttonFrame,width=5).grid(row=0,column=0)
        self.backBtn = tk.Button(buttonFrame,text="Back", font=("Arial", "10", "bold"),command=lambda:self.gotoStartPage(controller),width=20)
        self.backBtn.grid(row = 0,column=1,sticky="news")

        tk.Label(buttonFrame,width=45).grid(row=0,column=2)

        self.uploadBtn = tk.Button(buttonFrame,text="Next", font=("Arial", "10", "bold"), command=lambda:self.addToHierarchy(self.filePath.get(),controller),width=20)
        self.uploadBtn.grid(row = 0,column=3,sticky="news")
        self.uploadBtn.tk_focusNext()
        # self.uploadBtn.focus()
        buttonFrame.grid(row=4,column=0,sticky="news")

    def getFileName(self):
        fileName = filedialog.askopenfilename(defaultextension = ".txt",filetypes = [("EDF File","*.edf"),("Patient File","*.dat"),("All Files","*.*")])
        self.filePath.set(fileName)
        return fileName
    
    def gotoStartPage(self,controller):
        FILESPATH[0]=''
        for key in controller.frames.keys():
                if key.__name__ == 'StartPage':
                    controller.showFrame(key)

    def addToHierarchy(self,fPath,controller):
        if fPath:
            for key in controller.frames.keys():
                if key.__name__ == 'StartPage':
                    StartPage = key

            #FILESPATH is used to pass data between upload and startpage via eegmain.py
            FILESPATH[0]=fPath            
            controller.showFrame(StartPage)
        else:
            messagebox.showwarning("Invalid File","Please select a valid file.")
