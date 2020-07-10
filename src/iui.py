# -*- coding: utf-8 -*-

import tkinter as tk  
import tkinter.ttk   as ttk           
from tkinter import font  as tkfont 
from tkinter import *
import cv2
from PIL import Image,ImageTk
import tensorflow as tf
import numpy as np
import sql_gestion
import time
import configparser
import os
import logging
from text_to_speech import *
from logging.handlers import RotatingFileHandler

# initialisation des vairable globale logger model ....

try :
    os.environ['KMP_DUPLICATE_LIB_OK']='True'

    config = configparser.ConfigParser()
    config.read('../config/config.ini')

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s-%(levelname)s-[%(message)s]')
    file_handler = RotatingFileHandler(config['GLOBAL_LOG_MONITORING']['log'] , 'a', 1000000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


    model = tf.keras.models.load_model(config['MODELS']['current'])

    list_all=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","space","nothing"]

    french = ["connexion","exit","Fichier","Compte","Connexion","Utiliser sans Connexion","Lettre détectée  : ", "Mots détectés  : ","Read Text",
    "Clear Text","Retour ","Email :","Mots de passe :","Se connecter","Inscription","l'email est vide !","le mot de passe est vide !" ,"vous etes connecter",
    "deconnexion","modifier mots de passe","email ou mots de passe incorrect","Nom :","Prenom :","Date de Naissance :","Email :","Mots de passe :","Confirmer :",
    "Inscription","Retour","le nom est vide !","le prenom est vide !","le email est vide !","le password est vide !","la confirmation est vide !",
    "le password n'est pas identique!","email deja utilier ","Translate","Retour","ALS TO TEXT","TEXT TO ASL","le date de naissance est vide !","outill administrateur"]


    language = config['LANGUAGE']['current']
    if language == "fr" :
        language = french
    else :
        language = french


    width, height = 900, 1300
    cap = cv2.VideoCapture(0)
    cap_region_x_begin=0.5  
    cap_region_y_end=0.8  

    logger.info("get model and init  ... OK ")

except Exception as e:
    logger.error("get model and init ... KO ")
    logger.error(f"The error '{e}' occurred")

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        # initialiser du controleur 
        try :
            tk.Tk.__init__(self, *args, **kwargs)

            self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
            self.title("Sign Language Translator")
            self.geometry("925x550")
            self.minsize(925,650)
            self.config(background='white')
            self.font= tkfont.Font(family="Times",size=15,weight = 'bold')
            menu =  Menu(self)
            self.config(menu=menu)
            self.current_user = {}

            file = Menu(menu,tearoff=0)
            file.add_command(label=language[1],font=self.font,command=lambda : self.exit())

            self.compte = Menu(menu,tearoff=0)
                
            menu.add_cascade(label=language[2] ,font=self.font, menu =file)
            menu.add_cascade(label=language[3] ,font=self.font, menu =self.compte)

            container = tk.Frame(self)
            container.pack(side="top", fill="both", expand=True)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            self.ckeck = False
            self.frames = {}
            for F in (StartPage, Conection,Cam_to_Text,Inscription,Choise_mode,Text_to_Asl):
                page_name = F.__name__
                frame = F(parent=container, controller=self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            
            self.compte.add_command(label=language[0],font=self.font,command=lambda: self.show_frame("Conection"))
            self.frame_cam = Frame(self.frames["Cam_to_Text"])
            self.lmain = Label(self.frame_cam)
            self.lmain.pack(side="top",expand=YES)
        
            self.show_frame("StartPage")
            logger.error("init controller... OK ")
        except Exception as e:
            logger.error("init controller... KO ")
            logger.error(f"The error '{e}' occurred")


    def exit(self):
        # cette fonction va quiter l'application et enregristre ce quit dans la table history
        try : 
            sql_gestion.add_entry(self.current_user["mail"],False)
            logger.error("exit controller ... OK ")
        except Exception as e:
            logger.error("exit controller ... KO ")
            logger.error(f"The error '{e}' occurred")
        self.quit()

    def show_frame(self, page_name):
        # cette fonction va afficher la fenetre en parametre

        try:
            '''Show a frame for the given page name'''
            self.update()
            frame = self.frames[page_name]
            frame.tkraise()
            if page_name == "Cam_to_Text" and self.ckeck == False :
                self.ckeck = True
                self.show_cam()
            logger.error("show_frame controller ... OK ")
        except Exception as e:
            logger.error("show_frame controller ... KO ")
            logger.error(f"The error '{e}' occurred")
            
    def deconetion(self):
        # cette fonction va deconecter l'utilisateur et enregristre ce quit dans la table history
        try :
            sql_gestion.add_entry(self.current_user["mail"],False)
            self.current_user={}
            self.compte.delete(1,2)
            self.show_frame("StartPage")
            logger.error("deconetion controller ... OK ")
        except Exception as e:
            logger.error("deconetion controller ... KO ")
            logger.error(f"The error '{e}' occurred")

    def show_cam(self):
        # cette fonction va activer la web cam et transmerte les images au model qui va les traiter 
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

        self.frames["Cam_to_Text"].current_letter.set("Lettre détectée  : " + list_all[np.argmax(arry)])

        self.frames["Cam_to_Text"].dict_counter[list_all[np.argmax(arry)]] +=   1

        for lettre in list_all :
            if self.frames["Cam_to_Text"].dict_counter[lettre] == 50 and lettre != "nothing":
                if lettre == "space" :
                    str = self.frames["Cam_to_Text"].text.get()+" "
                else :
                    str = self.frames["Cam_to_Text"].text.get()+lettre
                
                self.frames["Cam_to_Text"].text.set(str)
                self.frames["Cam_to_Text"].dict_counter = {x:0 for x in list_all}


        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)

        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        
        if self.ckeck == True :
            
            self.lmain.after(20, self.show_cam)
        else :
            
            self.frame_cam.pack_forget()
 
class StartPage(tk.Frame):
    # initialisation de la page start 
    def __init__(self, parent, controller):
        try :
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.config(background='white')
            lable = Label(self,borderwidth = 0, relief="flat" )
            imgtk = PhotoImage(file = "../resources/image_iu/front.png")
            
            lable.imgtk = imgtk
            lable.configure(image=imgtk)
            lable.pack()
                
            button = tk.Button(self, text=language[4] , font =controller.font, command=lambda: controller.show_frame("Conection"))
            button_2 = tk.Button(self, text=language[5] ,font =controller.font, command=lambda: controller.show_frame("Choise_mode"))
            button.pack(side="left", expand=True)
            button_2.pack(side='right', expand=True)
            logger.error("__init__ StartPage ... OK ")
        except Exception as e:
            logger.error("__init__ StartPage ... KO ")
            logger.error(f"The error '{e}' occurred")

class Cam_to_Text(tk.Frame):
    
    def __init__(self, parent, controller):
        # initialisation de la fenetre Cam_to_Text
        try : 
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.current_letter = StringVar()
            self.text =  StringVar()
            
            self.dict_counter = {x:0 for x in list_all}
            self.lmain = Label(self)
            self.lmain.pack(side="left")

            frame_text = Frame(self)

            self.label = tk.Label(frame_text, font=controller.font,textvariable=self.current_letter)
            self.current_letter.set(language[6])
            self.label.pack(side="top", fill="x", pady=10)

            self.label_mots = tk.Label(frame_text, font=controller.font,textvariable=self.text)
            self.text.set(language[7])
            self.label_mots.pack(side="top", fill="x", pady=10)
            frame_text.pack(side="top")


            frame_button = Frame(self)     
            
            button = tk.Button(frame_button, text=language[8],font=controller.font,
                            command=lambda: text_to_speech (self.text.get()))
            button.pack(side="left")

            button = tk.Button(frame_button, text=language[9],font=controller.font,
                            command=lambda: text_to_speech (self.text.set(language[7])))
            button.pack(side="right")
            frame_button.pack(side="top")

            button = tk.Button(self, text=language[10],font=controller.font,
                            command=lambda: self.stop_cam())
            button.pack(side="bottom")
            logger.error("__init__ Cam_to_Text ... OK ")
        except Exception as e:
            logger.error("__init__ Cam_to_Text ... KO ")
            logger.error(f"The error '{e}' occurred")

    def stop_cam (self):
        # cette fonction permer de stopper la camera
        try :
            self.controller.show_frame("Choise_mode")
            self.controller.update()
            self.ckeck = False
            cap.release()
            cap = cv2.VideoCapture(0)
            logger.error("stop_cam Cam_to_Text ... OK ")
        except Exception as e:
            logger.error("stop_cam Cam_to_Text ... KO ")
            logger.error(f"The error '{e}' occurred")

class Conection(tk.Frame):

    def __init__(self, parent, controller):
        # initialisation de la fenetre Conection
        try : 
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.config(background='white')
            lable = Label(self,borderwidth = 0, relief="flat")
            imgtk = PhotoImage(file = "../resources/image_iu/conect.png")
            lable.imgtk = imgtk
            lable.configure(image=imgtk)
            lable.pack(side="left",expand=YES)

            self.frame_right = Frame(self)
            frame_email = Frame(self.frame_right)

            lable_email = Label(frame_email,text=language[11],font=controller.font)
            email = Entry(frame_email,font=controller.font)

            frame_password = Frame(self.frame_right)

            lable_password = Label(frame_password,text=language[12],font=controller.font)
            password = Entry(frame_password,show="*",font=controller.font)

            lable_email.pack(side="left")
            email.pack(side="right",expand=YES)

            lable_password.pack(side="left")
            password.pack(side="right",expand=YES)


            frame_email.pack(side='top',expand=YES)
            frame_password.pack(side='top',expand=YES)

            frame_button = Frame(self.frame_right)
            
            button = tk.Button(frame_button, text=language[13],font=controller.font,
                            command=lambda: self.Conect(controller ,email.get(),password.get()))
            button.pack(side='left',expand=YES)

            self.lable_status = Label(self.frame_right,text="", font=controller.font)

            button_Inscription = tk.Button(frame_button, text=language[14],font=controller.font,
                            command=lambda: controller.show_frame("Inscription"))
            button_Inscription.pack(side='right',expand=YES)
            frame_button.pack(side='bottom',expand=YES)


            self.frame_right.pack(side="right")
            logger.error("__init__ Conection ... OK ")
        except Exception as e:
            logger.error("__init__ Conection ... KO ")
            logger.error(f"The error '{e}' occurred")

   
    def Conect(self , controller ,email,password):
        # cette fonction a pour but de recupere les valuer saisie par l utilisateur et de les comparer avec celles stocker dans la base de donnée
        try : 
            handicap="1"
            check = True
            if email == "" :
                check = False
                self.lable_status.pack_forget()
                self.lable_status = Label(self.frame_right,text=language[15],fg="red", font=controller.font)
                self.lable_status.pack(side='bottom',expand=YES)
            if password == "" :
                check = False     
                self.lable_status.pack_forget()   
                self.lable_status = Label(self.frame_right,text=language[16],fg="red", font=controller.font)
                self.lable_status.pack(side='bottom',expand=YES)
        

            if check :
                try :
                    mail , pas, nom , prenom , admin = sql_gestion.get_user(email)


                    if mail == email and pas == password :

                        self.lable_status.pack_forget()   
                        self.lable_status = Label(self.frame_right,text=language[17],fg="green", font=controller.font)
                        self.lable_status.pack(side='bottom',expand=YES)
                        controller.current_user = {'mail':mail,'password':password, 'nom':nom, 'prenom':prenom}


                        controller.compte.add_command(label=language[18],font=controller.font,command=lambda:  controller.deconetion())
                        if admin == 1 :
                            controller.compte.add_command(label=language[41],font=controller.font,command=lambda:  controller.show_frame("Admin"))
                        sql_gestion.add_entry(email,True)
                        controller.show_frame("Choise_mode")
                        time.sleep(0.5)
            
                    else :
                        self.lable_status.pack_forget()   
                        self.lable_status = Label(self.frame_right,text=language[20],fg="red", font=controller.font)
                        self.lable_status.pack(side='bottom',expand=YES)

                    logger.error("Conect Conection ... OK ")

                except Exception as e :
                    logger.error("Conect Conection ... KO ")
                    logger.error(f"The error '{e}' occurred")
                    self.lable_status.pack_forget()   
                    self.lable_status = Label(self.frame_right,text=language[20],fg="red", font=controller.font)
                    self.lable_status.pack(side='bottom',expand=YES)

            logger.error("Conect Conection ... OK ")
        except Exception as e:
            logger.error("Conect Conection ... KO ")
            logger.error(f"The error '{e}' occurred")
            
class Inscription(tk.Frame):

    def __init__(self, parent, controller):
        try :
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.config(background='white')
            lable = Label(self,borderwidth = 0, relief="flat")
            imgtk = PhotoImage(file = "../resources/image_iu/conect.png")
            lable.imgtk = imgtk
            lable.configure(image=imgtk)
            lable.pack(side="left",expand=YES)

            self.frame_right = Frame(self)
            

            frame_nom = Frame(self.frame_right)
            lable_nom = Label(frame_nom,text=language[21],font=controller.font)
            nom = Entry(frame_nom,font=controller.font)
            lable_nom.pack(side="left")
            nom.pack(side="right",expand=YES)



            frame_Prenom = Frame(self.frame_right)
            lable_prenom = Label(frame_Prenom,text=language[22],font=controller.font)
            prenom = Entry(frame_Prenom,font=controller.font)
            lable_prenom.pack(side="left")
            prenom.pack(side="right",expand=YES)




            frame_date_naissance = Frame(self.frame_right)
            lable_date_naissance = Label(frame_date_naissance,text=language[23],font=controller.font)
            date_naissance = Entry(frame_date_naissance,font=controller.font)
            lable_date_naissance.pack(side="left")
            date_naissance.pack(side="right",expand=YES)




            frame_email = Frame(self.frame_right)
            lable_email = Label(frame_email,text=language[24],font=controller.font)
            email = Entry(frame_email,font=controller.font)
            lable_email.pack(side="left")
            email.pack(side="right",expand=YES)




            frame_password = Frame(self.frame_right)
            lable_password = Label(frame_password,text=language[25],font=controller.font)
            password = Entry(frame_password,show="*",font=controller.font)
            lable_password.pack(side="left")
            password.pack(side="right",expand=YES)




            frame_password_check = Frame(self.frame_right)
            lable_password_check = Label(frame_password_check,text=language[26],font=controller.font)
            password_check = Entry(frame_password_check,show="*",font=controller.font)
            lable_password_check.pack(side="left")
            password_check.pack(side="right",expand=YES)



            frame_nom.pack(side='top',expand=YES)
            frame_Prenom.pack(side='top',expand=YES)
            frame_email.pack(side='top',expand=YES) 
            frame_date_naissance.pack(side="top",expand=YES)
            frame_password.pack(side='top',expand=YES)
            frame_password_check.pack(side='top',expand=YES)

            print(password_check.get())

            
            self.lable_status = Label(self.frame_right,text="", font=controller.font)
            
            frame_button = Frame(self.frame_right)

            button = tk.Button(frame_button, text=language[27],font=controller.font,
                            command=lambda: self.Inscrip(controller,nom.get(),prenom.get(),email.get(),password.get(),password_check.get(),date_naissance.get()))
            button.pack(side='left',expand=YES)

            button_1 = tk.Button(frame_button, text=language[28],font=controller.font,
                            command=lambda: controller.show_frame("StartPage"))

            button_1.pack(side='right',expand=YES)
            frame_button.pack(side='bottom',expand=YES)

            self.frame_right.pack(side="right")
            logger.error("__init__ Inscription ... OK ")
        except Exception as e:
            logger.error("__init__ Inscription ... KO ")
            logger.error(f"The error '{e}' occurred")


    def Inscrip(self , controller ,nom,prenom,email,password,password_check,date_naissance):
        try :
            handicap="1"
            check = True
            if nom == "" :
                check = False
                self.lable_status.pack_forget()
                self.lable_status = Label(self.frame_right,text=language[29],fg="red", font=controller.font)
                self.lable_status.pack(side='top',expand=YES)

            if prenom == "" and check == True :
                check = False
                self.lable_status.pack_forget()
                self.lable_status = Label(self.frame_right,text=language[30],fg="red", font=controller.font)
                self.lable_status.pack(side='top',expand=YES)

            if email == "" and check == True:
                check = False
                self.lable_status.pack_forget()
                self.lable_status = Label(self.frame_right,text=language[31],fg="red", font=controller.font)
                self.lable_status.pack(side='top',expand=YES)

            if date_naissance == ""  and check == True:
                check = False
                self.lable_status.pack_forget()
                self.lable_status = Label(self.frame_right,text=language[40],fg="red", font=controller.font)
                self.lable_status.pack(side='top',expand=YES)

            if password == ""  and check == True:
                check = False
                self.lable_status.pack_forget()
                self.lable_status = Label(self.frame_right,text=language[32],fg="red", font=controller.font)
                self.lable_status.pack(side='top',expand=YES)

            if password_check == "" and check == True :
                check = False
                self.lable_status.pack_forget()
                self.lable_status = Label(self.frame_right,text=language[33],fg="red", font=controller.font)
                self.lable_status.pack(side='top',expand=YES)

            if password_check != password and check == True  :
                check = False
                self.lable_status.pack_forget()
                self.lable_status = Label(self.frame_right,text=language[34],fg="red", font=controller.font)
                self.lable_status.pack(side='top',expand=YES)
        
            if check :
                result = sql_gestion.add_user(nom,prenom,email,password,date_naissance,handicap)

                if result :
                    controller.show_frame("Conection")
                
                else :
                    self.lable_status.pack_forget()
                    self.lable_status = Label(self.frame_right,text=language[35],fg="red", font=controller.font)
                    self.lable_status.pack(side='top',expand=YES)

            logger.error("__init__ Inscription ... OK ")
        except Exception as e:
            logger.error("__init__ Inscription ... KO ")
            logger.error(f"The error '{e}' occurred")

class Text_to_Asl(tk.Frame):

    def __init__(self, parent, controller):
        try :  
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.v = StringVar()
            self.v.set("hello tous le monde")

            self.frame_right = Frame(self)
            self.frame_left = Frame(self)
            
            self.text = Entry(self.frame_left,textvariable=self.v,font=controller.font )
            self.text.pack()
            self.button =  tk.Button(self.frame_left, text=language[36],font=controller.font,
                            command=lambda: self.translate(self.text.get().lower()))
            self.button.pack(side='left',expand=YES)

            self.button =  tk.Button(self.frame_left, text=language[37],font=controller.font,
                            command=lambda: controller.show_frame("Choise_mode"))
            self.button.pack(side='left',expand=YES)



            self.frame_right.pack(side="right",expand=YES)
            self.frame_left.pack(side="left",expand=YES)
            self.lable = Label(self.frame_right, borderwidth = 0, relief="flat")
            self.translate("hello tous le monde")
            logger.error("__init__ Text_to_Asl ... OK ")

        except Exception as e:
            logger.error("__init__ Text_to_Asl ... KO ")
            logger.error(f"The error '{e}' occurred")


    def translate(self,text):
        try :
            self.frame_right.pack_forget()
            self.frame_right = Frame(self)
            self.frame_right.pack(side="right",expand=YES)

            for mots in text.split(" ") :
                frame = Frame(self.frame_right)
                for elt in mots :
                    self.lable = Label(frame,borderwidth = 0, relief="flat")
                    imgtk = PhotoImage(file = "../resources/image_iu/"+elt+".png")
                    self.lable.imgtk = imgtk
                    self.lable.configure(image=imgtk)
                    self.lable.pack(side="left",expand=YES)
                frame.pack()

            self.v.set("")
            logger.error("translate Text_to_Asl ... OK ")

        except Exception as e:
            logger.error("translate Text_to_Asl ... KO ")
            logger.error(f"The error '{e}' occurred")

class Choise_mode(tk.Frame):
    def __init__(self, parent, controller):
        try : 
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.config(background='white')

            lable = Label(self,borderwidth = 0, relief="flat")
            imgtk = PhotoImage(file = "../resources/image_iu/conect.png")
            lable.imgtk = imgtk
            lable.configure(image=imgtk)
            lable.pack(side="left",expand=YES)

            self.frame_right = Frame(self)
            
            button = tk.Button(self.frame_right, text=language[38],font=controller.font,
                            command=lambda: controller.show_frame("Cam_to_Text"))
            button.pack(side="top",expand=YES)

            button = tk.Button(self.frame_right, text=language[39],font=controller.font,
                            command=lambda: controller.show_frame("Text_to_Asl"))
            button.pack(side="bottom",expand=YES)
    
            self.frame_right.pack(side="right",expand=YES)
            logger.error("__init__ Choise_mode ... OK ")

        except Exception as e:
            logger.error("__init__ Choise_mode ... KO ")
            logger.error(f"The error '{e}' occurred")

if __name__ == "__main__":

    app = SampleApp()
    app.mainloop()