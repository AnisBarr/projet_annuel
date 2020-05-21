     # currentFrame.pack_forget()


import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2
from tkinter import *
import cv2
from PIL import Image,ImageTk

from tk_web_2 import *



width, height = 800, 600
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)



class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("Sign Language Translator")
        self.geometry("925x550")
        self.minsize(925,650)
        # self.maxsize(833,636)
        self.config(background='white')
        self.font= tkfont.Font(family="Lucida Grande",size=15,weight = 'bold')
        menu =  Menu(self)
        self.config(menu=menu)

        file = Menu(menu,tearoff=0)
        file.add_command(label="exit",font=self.font,command= self.quit)

        compte = Menu(menu,tearoff=0)
        compte.add_command(label="conection",font=self.font,command= self.quit)
        compte.add_command(label="deconection",font=self.font,command= self.quit)
        compte.add_command(label="modifier mots de passe",font=self.font,command= self.quit)
        compte.add_command(label="suprimer compte",font=self.font,command= self.quit)
       
        menu.add_cascade(label="Fichier" ,font=self.font, menu =file)
        menu.add_cascade(label="Compte" ,font=self.font, menu =compte)

        self.frame_cam = Frame(self)
        self.lmain = Label(self.frame_cam)
        self.lmain.pack()


        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne,PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
         
        self.frame_cam = Frame(self.frames["PageTwo"])
        self.lmain = Label(self.frame_cam)
        self.lmain.pack()
        
        self.show_frame("StartPage")


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        


        

    def show_cam(self):
        self.frame_cam.pack()
        self.frame_cam.tkraise()
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(10, self.show_cam)


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(background='white')
        lable = Label(self,borderwidth = 0, relief="flat" )
        imgtk = PhotoImage(file = "../resources/final4$.png")
        
        lable.imgtk = imgtk
        lable.configure(image=imgtk)
        lable.pack()
               
        font = tkfont.Font(family="calibri",size=15,weight = 'bold')

        button = tk.Button(self, text="Conection" , font =font,command=lambda: controller.show_frame("PageOne"))
        button_2 = tk.Button(self, text="Utiliser sans Conection" ,font =font,command=lambda: controller.show_frame("PageTwo"))
        button.pack(side="left", expand=True)
        button_2.pack(side='right', expand=True)






class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config(background='white')
        lable = Label(self,borderwidth = 0, relief="flat")
        imgtk = PhotoImage(file = "../resources/conect.png")
        lable.imgtk = imgtk
        lable.configure(image=imgtk)
        lable.pack(side="left")

        frame_right = Frame(self)
        frame_email = Frame(frame_right)

        lable_email = Label(frame_email,text="Email :",font=controller.font)
        email = Entry(frame_email,font=controller.font)

        frame_password = Frame(frame_right)

        lable_password = Label(frame_password,text="Mots de passe :",font=controller.font)
        password = Entry(frame_password,show="*",font=controller.font)

        lable_email.pack(side="left")
        email.pack(side="right",expand=YES)

        lable_password.pack(side="left")
        password.pack(side="right",expand=YES)


        frame_email.pack(side='top',expand=YES)
        frame_password.pack(side='top',expand=YES)
        
        button = tk.Button(frame_right, text="conect",font=controller.font,
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(side='bottom',expand=YES)

        frame_right.pack(side="right")

    

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2")
        label.pack(side="top", fill="x", pady=10)
 
        button_2 = tk.Button(self, text="Go ",
                           command=lambda: controller.show_cam())
        button_2.pack()

    

        


if __name__ == "__main__":

    app = SampleApp()
    app.mainloop()