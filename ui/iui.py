     # currentFrame.pack_forget()


import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2
from tkinter import *
import cv2
from PIL import Image,ImageTk
import tensorflow as tf
import numpy as np



model = tf.keras.models.load_model("/home/anis/hdd/stockage/projet_annuel/logs/mo_rnn_aug_True_act_relu_do_0.2_l2_0.001_op_adam_lr_0.001_mome_0.01_21-05-2020_19:06:38/my_model_acc_0.9903726.h5")
list_all=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","space","nothing"]
width, height = 800, 600
cap = cv2.VideoCapture(0)
cap_region_x_begin=0.5  # start point/total width
cap_region_y_end=0.8  # start point/total width
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)



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

        # self.frame_cam = Frame(self)
        # self.lmain = Label(self.frame_cam)
        # self.lmain.pack(side="left")


        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        

        self.ckeck = False
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
        self.lmain.pack(side="left")
        
        self.show_frame("StartPage")


    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
        if page_name == "PageTwo" and self.ckeck == False :
            self.ckeck = True
            self.show_cam()
            # cap = cv2.VideoCapture(0)
            
        
            
        


        

    def show_cam(self):
        self.frame_cam.pack()
        self.frame_cam.tkraise()
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)


        cv2.rectangle(frame, (int(cap_region_x_begin * frame.shape[1]), 0),
                 (frame.shape[1], int(cap_region_y_end * frame.shape[0])), (255, 0, 0), 2)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)


        img_predict = frame
        img_predict = img_predict[0:int(cap_region_y_end * frame.shape[0]),
                    int(cap_region_x_begin * frame.shape[1]):frame.shape[1]]  # clip the ROI
        img_predict = Image.fromarray(img_predict)
        img_predict = img_predict.convert("L")

        resized = img_predict.resize((64, 64), Image.ANTIALIAS)
        resized = np.asarray(resized)
        resized = np.reshape(resized,(-1,64,64,1))


        data = np.asarray(resized, dtype = "float32")/255
        arry = model.predict(data)
        self.frames["PageTwo"].v.set(list_all[np.argmax(arry)])

        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        
        if self.ckeck == True :
            
            self.lmain.after(20, self.show_cam)
        else :
            
            self.frame_cam.pack_forget()



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
                           command=lambda: controller.show_frame("PageTwo"))
        button.pack(side='bottom',expand=YES)

        frame_right.pack(side="right")

    

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.v = StringVar()
        
        self.label = tk.Label(self, textvariable=self.v)
        self.v.set("New Text!")
        self.label.pack(side="top", fill="x", pady=10)
 
        # button_2 = tk.Button(self, text="Go ",
        #                    command=lambda: controller.show_cam())
        # button_2.pack()
        button = tk.Button(self, text="Go ",
                           command=lambda: self.stop_cam())
        button.pack()
    

    def stop_cam (self):
        self.controller.show_frame("StartPage")
        self.ckeck = False
        cap.release ()


if __name__ == "__main__":

    app = SampleApp()
    app.mainloop()