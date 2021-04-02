import tkinter as tk
from tkinter import messagebox, ttk
import multiprocessing

from loginpage import Login
from startpage import StartPage
from resultpage import Results
from uploadpage import FILESPATH, Upload


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.browsingHistory = []
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.title(self, "EEG Assessment System")
        width = 750
        height = 450
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        tk.Tk.resizable(self, 0, 0)

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

    def showFrame(self, frameclass, *args):
        self.browsingHistory.append(frameclass)
        if frameclass in self.frames.keys():
            # print("You are in "+frameclass.__name__)
            # get the instance of frameclass
            f = self.frames[frameclass]
            # if frame is of StartPage update the file hierarchy and the raise it to top
            if frameclass.__name__ == 'StartPage':
                if self.browsingHistory[-2].__name__ == 'Results':
                    pass
                else:
                    for file in FILESPATH:
                        if len(file) > 0:
                            try:
                                f.insertIntoHierarchy(parent='', filePath=file)
                            except:
                                messagebox.showwarning(
                                    'Already Exist', 'The file you seleceted already exist in the file hierarchy.')
            elif frameclass.__name__ == 'Upload':
                f.filePath.set('')
            elif frameclass.__name__ == 'Results':  # error has to be solved from here
                self.frames[frameclass].initUI(args)
                # frameclass.initUI(args)
            f.tkraise()
        else:
            frame = frameclass(self.container, self, args)
            self.frames[frameclass] = frame
            frame.grid(row=0, column=0, sticky='news')
            frame.tkraise()

    def center(self, width, height):
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry('{}x{}+{}+{}'.format(width, height, x, y))


def main():
    f = open("firstTime.txt", mode="r")
    lines = f.read().splitlines()
    isFirstTime = int(lines[0].split("=")[1])
    hospitalName = lines[1].split("=")[1]
    f.close()

    mainapp = MainApp()
    mainapp.title("EEG Assessment System - "+str(hospitalName))
    mainapp.showFrame(Login)

    if isFirstTime == 1:
        mainapp.showFrame(Login)
    else:
        mainapp.showFrame(StartPage)
    mainapp.mainloop()


if __name__ == "__main__":
    main()
