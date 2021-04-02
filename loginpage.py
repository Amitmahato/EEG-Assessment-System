import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox

from startpage import StartPage


class Login(tk.Frame):
    def __init__(self,parent,controller,*args):
        tk.Frame.__init__(self,parent)
        # self.__master = tk.Tk()
        # self.__master.config(height=450,width=750)
        # self.__master.title("EEG Assessment System")   #here goes the location of icon file 
        
        self.__customFont = tkFont.Font(family="Times", size=18, slant="italic")
        
        # greetingFont = tkFont.Font(family="Sans Serif", size=30, slant = "italic", weight="bold")
        # self.__greetingLabel = tk.Label(self.__master, compound=tk.CENTER, text="Welcome!", font=greetingFont)
        # self.__greetingLabel.place(relx=0.5,y=35,anchor="center")
        
        self.__logoImg = tk.PhotoImage(file="./static/logo1_1.png")
        self.__logoLabel = tk.Label(self, compound=tk.CENTER, image=self.__logoImg)
        self.__logoLabel.place(relx=0.5, y=150, anchor=tk.CENTER)
        #let y=150 for without greeting text and 210 with greeting text
        
        self.__hospitalNameLabel = tk.Label(self,text="Enter Hospital Name   : ", font=self.__customFont)
        self.__hospitalNameLabel.place(relx=0.33,rely=0.8,anchor=tk.CENTER)
        
        self.hospitalName = tk.StringVar()
        entryFont = tkFont.Font(family="Helvetica",size=15)
        self.__hospitalNameEntry = tk.Entry(self,textvariable=self.hospitalName, font=entryFont)
        self.__hospitalNameEntry.config(width=22,relief=tk.SUNKEN,justify=tk.LEFT)
        self.__hospitalNameEntry.place(relx=0.73,rely=0.8,anchor=tk.CENTER)
        self.__hospitalNameEntry.selection_range(0,tk.END)

        self.__enterBtn = tk.Button(self,text="Enter", font=("Arial", "10", "bold"),width=10 , command=lambda:self.proceed(controller))
        self.__enterBtn.place(relx=0.5,rely=0.93,anchor=tk.CENTER)
    
    def __validName(self):
        if len(self.hospitalName.get()) > 1:
            return True
        return False
    
    def proceed(self,controller):
        if self.__validName():
            controller.showFrame(StartPage)
            f = open("firstTime.txt",mode="w")
            f.write("FIRSTTIME=0\nHOSPITALNAME={}".format(self.hospitalName.get()))
        else:
            messagebox.showerror('Unfilled','Please provide a valid hospital name.')
