import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter.messagebox import *

from Abstraction import Abstraction

class Results(tk.Frame):
    def __init__(self,parent,controller,args):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.initUI(args)

    def initUI(self,args):
        self.customFont = tkFont.Font(family="Times", size=14)
        
        channelFrame = tk.Frame(self,width=250,height=450,bg='white smoke',padx=0,pady=10,bd=4)
        header = tk.Frame(channelFrame,bg='gray',padx=10)
        tk.Label(header,bg='lightgray',font=self.customFont,text="Channel Status").pack(fill="both",expand=True,anchor="center",ipadx=40)
        header.grid(row=0,column=0)

        body = tk.Frame(channelFrame,width=250,height=400,padx=16)
        self.channelList = tk.Listbox(body,height=20,width=25,font=("Times",12))
        self.channelList.grid(row=0,column=0)
        
        processedData = args[0]
        self.channelName = processedData.channelName
        self.channelStatus = processedData.result

        self.channelList.delete(0,"end")
        for i in range(32):
            if(i<10):
                self.channelList.insert(i,"     Channel    {}   :   {}".format(self.channelName[i],self.channelStatus[i]))
            else:
                self.channelList.insert(i,"     Channel    {}   :   {}".format(self.channelName[i],self.channelStatus[i]))

        self.scrollBar = tk.Scrollbar(body,width=12)
        self.scrollBar.grid(row = 0, column=1)
        self.scrollBar.grid(sticky="ns")

        #bind the displayResult with the scrollbar so as to let the scrollbar control displayResult view
        self.channelList.configure(yscrollcommand = self.scrollBar.set)
        self.scrollBar.configure(command = self.channelList.yview)

        body.grid(row=1,column=0)
        body.grid_propagate(False)
        #create a scrollbar and place it right side of displayResult area
        channelFrame.grid(row=0,column=0)
        channelFrame.grid_propagate(False)
        
        powerFrame = tk.Frame(self,width=500,height=450,bg='white smoke',padx=0,pady=10,bd=4)
        frequencyFrame = tk.Frame(powerFrame,pady=0)

        headerFreq = tk.Frame(frequencyFrame,width=500,bg='gray',padx=140)
        tk.Label(headerFreq,font=self.customFont,text="Frequency Distribution",padx=10).pack(fill="both", anchor="center")
        headerFreq.grid(row=0,column=0,columnspan=5)
        # headerFreq.grid_propagate("False")

        tk.Label(frequencyFrame,font=self.customFont,text="Frequency Between").grid(row=1,column=0)
        tk.Label(frequencyFrame,font=self.customFont,text="Frequency Between").grid(row=2,column=0)
        tk.Label(frequencyFrame,font=self.customFont,text="Frequency Between").grid(row=3,column=0)
        tk.Label(frequencyFrame,font=self.customFont,text="Frequency Between").grid(row=4,column=0)

        
        tk.Label(frequencyFrame,font=self.customFont,text="0  to 8     ").grid(row=1,column=1)
        tk.Label(frequencyFrame,font=self.customFont,text="8  to 15    ").grid(row=2,column=1)
        tk.Label(frequencyFrame,font=self.customFont,text="15 to 60    ").grid(row=3,column=1)
        tk.Label(frequencyFrame,font=self.customFont,text="more than 60").grid(row=4,column=1)


        tk.Label(frequencyFrame,font=self.customFont,text=" : ").grid(row=1,column=2,padx=10)
        tk.Label(frequencyFrame,font=self.customFont,text=" : ").grid(row=2,column=2)
        tk.Label(frequencyFrame,font=self.customFont,text=" : ").grid(row=3,column=2)
        tk.Label(frequencyFrame,font=self.customFont,text=" : ").grid(row=4,column=2)

        self.__fb0_8 = tk.Label(frequencyFrame,font=self.customFont,text="0", padx=50)
        self.__fb0_8.grid(row=1,column=3)

        self.__fb8_15 = tk.Label(frequencyFrame,font=self.customFont,text="0")
        self.__fb8_15.grid(row=2,column=3)

        self.__fb15_60 = tk.Label(frequencyFrame,font=self.customFont,text="0")
        self.__fb15_60.grid(row=3,column=3)

        self.__fgt60 = tk.Label(frequencyFrame,font=self.customFont,text="0")
        self.__fgt60.grid(row=4,column=3)
        
        self.setResult(processedData)
        frequencyFrame.grid(row=0,column=0,rowspan=2)

        # tk.Label(powerFrame,font=self.customFont,text="EEG Length : ").grid(row = 2,column=0,pady=10)
        # tk.Label(powerFrame,font=self.customFont,text="").grid(row=2,column=1,pady=10)
        # eegLen = tk.Label(powerFrame,font=self.customFont,text="1s",pady=10)
        # eegLen.grid(row=2,column=1)

        back = tk.Button(powerFrame,text="Back",width=10,font=("Times",15),bg='slate blue',relief="raised",command=self.gotoStartPage)
        back.place(relx=0.1,rely=0.96,anchor="center")
        plot3d = tk.Button(powerFrame,text="Generate 3D Model",width=33,font=("Times",15),bg='slate blue',relief="raised",command=lambda:processedData.render())
        plot3d.place(relx=0.62,rely=0.96,anchor="center")
        powerFrame.grid(row=0,column=1)
        powerFrame.grid_propagate(False)

    def popupResult(self):
        result = "Pass" if int(self.__fgt60['text'][:-1])>10 else "Fail"
        showinfo("Result",result)

    def setResult(self,obj):
        # self.totalTimeValue['text'] = str(obj.eegLength)+'s'
        # print(obj.eegLength)

        self.__fb0_8['text'] = str(obj.powers[0].__round__(2))
        self.__fb8_15['text'] = str(obj.powers[1].__round__(2))
        self.__fb15_60['text'] = str(obj.powers[2].__round__(2))
        self.__fgt60['text'] = str(obj.powers[3].__round__(2))
    
    def gotoStartPage(self):
        for key in self.controller.frames.keys():
                if key.__name__ == 'StartPage':
                    self.controller.showFrame(key)
