# -*- coding: utf-8 -*-

import tkinter as tk  
import tkinter.ttk   as ttk           
from tkinter import font  as tkfont 
from tkinter import *
from tkinter import filedialog
import cv2
from PIL import Image,ImageTk
import tensorflow as tf
import numpy as np
import configparser
import os
import time
import logging
from beautifultable import BeautifulTable
import sql_gestion
from text_to_speech import *
import trying_model 
from logging.handlers import RotatingFileHandler
from tensorboard.plugins.hparams import api as hp

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
    "le password n'est pas identique!","email deja utilier ","Translate","Retour","ALS TO TEXT","TEXT TO ASL","le date de naissance est vide !","outils administrateur","changer de model",
    "consuleter la BD","lancer la requete","la requete :", "selection un model" ,"importer","model a etait imoprter et changer","erreur chargement model","entrainer un model","structure du model : ","optimaizer : ",
    "learing_rate","L2 regularitaion : ","fonction d'activation : ", "drop out : ", "batch size :", "epochs :","Lancer le train", "erreur de lancement, lancer avec parametre par defaut"]


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
            for F in (StartPage, Conection,Cam_to_Text,Inscription,Choise_mode,Text_to_Asl,Choise_admin,Sql_query,Change_model,Change_model,Train_model):
                page_name = F.__name__
                frame = F(parent=container, controller=self)
                self.frames[page_name] = frame
                frame.grid(row=0, column=0, sticky="nsew")
            
            self.compte.add_command(label=language[0],font=self.font,command=lambda: self.show_frame("Conection"))
            self.frame_cam = Frame(self.frames["Cam_to_Text"])
            self.lmain = Label(self.frame_cam)
            self.lmain.pack(side="top",expand=YES)
        
            self.show_frame("StartPage")
            logger.info("init controller... OK ")
        except Exception as e:
            logger.error("init controller... KO ")
            logger.error(f"The error '{e}' occurred")

    def exit(self):
        # cette fonction va quiter l'application et enregristre ce quit dans la table history
        try : 
            sql_gestion.add_entry(self.current_user["mail"],False)
            logger.info("exit controller ... OK ")
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
            logger.info("show_frame controller ... OK ")
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
            logger.info("deconetion controller ... OK ")
        except Exception as e:
            logger.error("deconetion controller ... KO ")
            logger.error(f"The error '{e}' occurred")

    def show_cam(self):
        # cette fonction va activer la web cam et transmerte les images au model qui va les traiter 
        try :
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
            logger.info("show_cam controller ... OK ")
        except Exception as e:
            logger.error("show_cam controller ... KO ")
            logger.error(f"The error '{e}' occurred")


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
            logger.info("__init__ StartPage ... OK ")
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
            logger.info("__init__ Cam_to_Text ... OK ")
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
            logger.info("stop_cam Cam_to_Text ... OK ")
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
            self.email = Entry(frame_email,font=controller.font)

            frame_password = Frame(self.frame_right)

            lable_password = Label(frame_password,text=language[12],font=controller.font)
            self.password = Entry(frame_password,show="*",font=controller.font)

            lable_email.pack(side="left")
            self.email.pack(side="right",expand=YES)

            lable_password.pack(side="left")
            self.password.pack(side="right",expand=YES)


            frame_email.pack(side='top',expand=YES)
            frame_password.pack(side='top',expand=YES)

            frame_button = Frame(self.frame_right)
            
            button = tk.Button(frame_button, text=language[13],font=controller.font,
                            command=lambda: self.Conect(controller ,self.email.get(),self.password.get()))
            button.pack(side='left',expand=YES)

            self.lable_status = Label(self.frame_right,text="", font=controller.font)

            button_Inscription = tk.Button(frame_button, text=language[14],font=controller.font,
                            command=lambda: controller.show_frame("Inscription"))
            button_Inscription.pack(side='right',expand=YES)
            frame_button.pack(side='bottom',expand=YES)


            self.frame_right.pack(side="right")
            logger.info("__init__ Conection ... OK ")
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
                            controller.compte.add_command(label=language[41],font=controller.font,command=lambda:  controller.show_frame("Choise_admin"))
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

            logger.info("Conect Conection ... OK ")
        except Exception as e:
            logger.error("Conect Conection ... KO ")
            logger.error(f"The error '{e}' occurred")


class Inscription(tk.Frame):

    def __init__(self, parent, controller):
        # initialisation de la fenetre Inscription
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
            logger.info("__init__ Inscription ... OK ")
        except Exception as e:
            logger.error("__init__ Inscription ... KO ")
            logger.error(f"The error '{e}' occurred")


    def Inscrip(self , controller ,nom,prenom,email,password,password_check,date_naissance):
        # cette fonction a pour but de recupere les valuer saisie par l utilisateur et de les stocker dans la base de donnée
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
                result = sql_gestion.add_user(nom,prenom,email,password,date_naissance)

                if result :
                    controller.show_frame("Conection")
                
                else :
                    self.lable_status.pack_forget()
                    self.lable_status = Label(self.frame_right,text=language[35],fg="red", font=controller.font)
                    self.lable_status.pack(side='top',expand=YES)

            logger.info("__init__ Inscription ... OK ")
        except Exception as e:
            logger.error("__init__ Inscription ... KO ")
            logger.error(f"The error '{e}' occurred")


class Text_to_Asl(tk.Frame):

    def __init__(self, parent, controller):
        # initialisation de la fenetre Text_to_Asl
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
            logger.info("__init__ Text_to_Asl ... OK ")

        except Exception as e:
            logger.error("__init__ Text_to_Asl ... KO ")
            logger.error(f"The error '{e}' occurred")


    def translate(self,text):
        #cette fonction va traduire le text en suite d'image
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
            logger.info("translate Text_to_Asl ... OK ")

        except Exception as e:
            logger.error("translate Text_to_Asl ... KO ")
            logger.error(f"The error '{e}' occurred")


class Choise_mode(tk.Frame):
    def __init__(self, parent, controller):
         # initialisation de la fenetre Choise_mode cette fenetre fa 
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
            logger.info("__init__ Choise_mode ... OK ")

        except Exception as e:
            logger.error("__init__ Choise_mode ... KO ")
            logger.error(f"The error '{e}' occurred")


class Choise_admin(tk.Frame):

    def __init__(self, parent, controller):
         # initialisation de la fenetre Choise_mode cette fenetre fa 
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
            
            button = tk.Button(self.frame_right, text=language[43],font=controller.font,
                            command=lambda: controller.show_frame("Sql_query"))
            button.pack(side="top",expand=YES)

            button = tk.Button(self.frame_right, text=language[42],font=controller.font,
                            command=lambda: controller.show_frame("Change_model"))
            button.pack(side="top",expand=YES)

            button = tk.Button(self.frame_right, text=language[50],font=controller.font,
                            command=lambda: controller.show_frame("Train_model"))
            button.pack(side="top",expand=YES)    
            
    
            self.frame_right.pack(side="right",expand=YES)
            logger.info("__init__ Choise_admin ... OK ")

        except Exception as e:
            logger.error("__init__ Choise_admin ... KO ")
            logger.error(f"The error '{e}' occurred")


class Sql_query(tk.Frame):

    def __init__(self, parent, controller):
        # initialisation de la fenetre Text_to_Asl
        try :  
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.v = StringVar()
            self.result = StringVar()

            self.frame_query = Frame(self)
            self.frame_button = Frame(self)
            self.frame_result = Frame(self)
            

            self.lablel_query = Label(self.frame_query, text=language[45] ,font =controller.font ,borderwidth = 0, relief="flat")
            self.text = Entry(self.frame_query,textvariable=self.v,font=controller.font ,width=70)
            self.lablel_query.pack(side="left")
            self.text.pack()


            self.button =  tk.Button(self.frame_button, text=language[44],font=controller.font,
                            command=lambda: self.query(self.v.get()))
            self.button.pack(side='left',expand=YES)

            self.button =  tk.Button(self.frame_button, text=language[37],font=controller.font,
                            command=lambda: controller.show_frame("Choise_admin"))
            self.button.pack(side='right',expand=YES)

            # canvas = Canvas(self.frame_result)
            # scrollbar = Scrollbar(self.frame_result, orient="vertical", command=canvas.yview)
            # scrollable_frame = Frame(canvas)
            # scrollable_frame.bind(
            #     "<Configure>",
            #     lambda e: canvas.configure(
            #         scrollregion=canvas.bbox("all")
            #     )
            # )
            # canvas.create_window((0, 0), window=scrollable_frame)
            # canvas.configure(yscrollcommand=scrollbar.set)


            self.lable = Label(self.frame_result,textvariable=self.result, font=controller.font, borderwidth = 0, relief="flat")
            self.lable.pack(expand=YES)

            
            self.frame_query.pack(side="top")
            self.frame_button.pack(side="top")
            self.frame_result.pack(side="top",expand=YES)
            # canvas.pack(side="left", fill="both", expand=True)
            # scrollbar.pack(side="right", fill="y", expand=True)

            logger.info("__init__ Sql_query ... OK ")

        except Exception as e:
            logger.error("__init__ Sql_query ... KO ")
            logger.error(f"The error '{e}' occurred")


    def query(self,text):
        #cette fonction va traduire le text en suite d'image
        try :

            query_result = sql_gestion.get_query(text)
            table = BeautifulTable()
            for row in query_result :
                table.append_row(row)
            
            self.result.set(str(table))
           
            logger.info("query Text_to_Asl ... OK ")

        except Exception as e:
            logger.error("query Text_to_Asl ... KO ")
            logger.error(f"The error '{e}' occurred")


class Change_model(tk.Frame):

    def __init__(self, parent, controller):
        # initialisation de la fenetre Change_model

        try :  
            tk.Frame.__init__(self, parent)
            self.controller = controller


            self.result = StringVar()
            # 46 = selection un model
            # 47 = importer
            # 48 = model a etait imoprter et changer 

            self.frame_query = Frame(self)

            self.lablel_query = Label(self.frame_query, text=language[46] ,font =controller.font ,borderwidth = 0, relief="flat")
            self.lablel_query.pack(side='left',expand=YES)

            self.button =  tk.Button(self.frame_query, text=language[47],font=controller.font, command=lambda: self.load_and_change(controller))
            self.button.pack(side='right',expand=YES)

            self.frame_query.pack(expand=YES)

            self.lablel_result = Label(self.frame_query, textvariable=self.result ,fg="green" ,font =controller.font ,borderwidth = 0, relief="flat")
            self.lablel_result.pack("bottom",expand=YES)
            self.lablel_query.pack(side='left',expand=YES)


            logger.info("__init__ Sql_query ... OK ")

        except Exception as e:
            logger.error("__init__ Sql_query ... KO ")
            logger.error(f"The error '{e}' occurred")


    def load_and_change(self,controller):
        try:
            self.result.set(" ")
            filename = filedialog.askopenfilename()
            os.system("cp "+filename+ " ../models")
            print(filename)
            name = os.path.split(filename)[-1]

            config.set('MODELS', 'old', config['MODELS']['current'])
            config.set('MODELS', 'current', '../models/'+name)
            self.result.set(language[48])
            print(config['MODELS']['current'])

            model = tf.keras.models.load_model(config['MODELS']['current'])

            time.sleep(1)

            controller.show_frame("Choise_admin")

            logger.info("load_and_chnage Change_model ... OK ")

        except Exception as e:
            self.result.set(language[49])
            logger.error("load_and_chnage Change_model ... KO ")
            logger.error(f"The error '{e}' occurred")


class Train_model(tk.Frame):

    def __init__(self, parent, controller):
        # initialisation de la fenetre Inscription
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
            
            text_structure =" 1 : model dense 2 layers \n 2 : model dense 3 layers \n 3 : model RNN 3 layers \n 4 : model Resnet 20 layers"

            lable_structure_info = Label(self.frame_right,text=text_structure,font=controller.font)
            lable_structure_info.pack(side='top',expand=YES)

            frame_structure = Frame(self.frame_right)
            lable_structure = Label(frame_structure,text=language[51],font=controller.font)
            structure = Entry(frame_structure,font=controller.font)
            lable_structure.pack(side="left")
            structure.pack(side="right",expand=YES)


            frame_optimaizer = Frame(self.frame_right)
            lable_optimaizer = Label(frame_optimaizer,text=language[52],font=controller.font)
            optimaizer = Entry(frame_optimaizer,font=controller.font)
            lable_optimaizer.pack(side="left")
            optimaizer.pack(side="right",expand=YES)


            frame_learing_rate = Frame(self.frame_right)
            lable_learing_rate = Label(frame_learing_rate,text=language[53],font=controller.font)
            learing_rate = Entry(frame_learing_rate,font=controller.font)
            lable_learing_rate.pack(side="left")
            learing_rate.pack(side="right",expand=YES)


            frame_regularitaion = Frame(self.frame_right)
            lable_regularitaion = Label(frame_regularitaion,text=language[54],font=controller.font)
            regularitaion = Entry(frame_regularitaion,font=controller.font)
            lable_regularitaion.pack(side="left")
            regularitaion.pack(side="right",expand=YES)


            frame_activation = Frame(self.frame_right)
            lable_activation = Label(frame_activation,text=language[55],font=controller.font)
            activation = Entry(frame_activation,font=controller.font)
            lable_activation.pack(side="left")
            activation.pack(side="right",expand=YES)


            frame_drop_out = Frame(self.frame_right)
            lable_drop_out = Label(frame_drop_out,text=language[56],font=controller.font)
            drop_out = Entry(frame_drop_out,font=controller.font)
            lable_drop_out.pack(side="left")
            drop_out.pack(side="right",expand=YES)


            frame_batch_size = Frame(self.frame_right)
            lable_batch_size = Label(frame_batch_size,text=language[57],font=controller.font)
            batch_size = Entry(frame_batch_size,font=controller.font)
            lable_batch_size.pack(side="left")
            batch_size.pack(side="right",expand=YES)


            frame_epochs = Frame(self.frame_right)
            lable_epochs = Label(frame_epochs,text=language[58],font=controller.font)
            epochs = Entry(frame_epochs,font=controller.font)
            lable_epochs.pack(side="left")
            epochs.pack(side="right",expand=YES)



            frame_structure.pack(side='top',expand=YES)
            frame_optimaizer.pack(side='top',expand=YES)
            frame_learing_rate.pack(side='top',expand=YES) 
            frame_regularitaion.pack(side="top",expand=YES)
            frame_activation.pack(side='top',expand=YES)
            frame_drop_out.pack(side='top',expand=YES)
            frame_batch_size.pack(side='top',expand=YES)
            frame_epochs.pack(side='top',expand=YES)

            
            self.lable_status = Label(self.frame_right,text="", font=controller.font)
            
            frame_button = Frame(self.frame_right)

            button = tk.Button(frame_button, text=language[59],font=controller.font,
                            command=lambda: self.train(controller,structure.get(),optimaizer.get(),learing_rate.get(),regularitaion.get(),activation.get(),drop_out.get(),batch_size.get(), epochs.get()))
            button.pack(side='left',expand=YES)

            button_1 = tk.Button(frame_button, text=language[28],font=controller.font,
                            command=lambda: controller.show_frame("Choise_admin"))

            button_1.pack(side='right',expand=YES)
            frame_button.pack(side='bottom',expand=YES)

            self.frame_right.pack(side="right")
            logger.info("__init__ Train_model ... OK ")
        except Exception as e:
            logger.error("__init__ Train_model ... KO ")
            logger.error(f"The error '{e}' occurred")

            # 51 = "structure du model : "
            # 52 = "optimaizer : "
            # 53 = "learing_rate"
            # 54 = "L2 regularitaion : "
            # 55 = "fonction d'activation : "
            # 56 = "drop out : "
            # 57 = "batch size :"
            # 58 = "epochs :"

    def train(self , controller ,structure,optimaizer,learing_rate,regularitaion,activation,drop_out,batch_size , epochs):
        # cette fonction a pour but de recupere les valuer saisie par l utilisateur et de les stocker dans la base de donnée
        try :

            METRIC_ACCURACY = 'accuracy'
            METRIC_LOSS='loss'
            log_dir='../logs/train/'

            HP_STRUCTURE= hp.HParam('structure_model', hp.Discrete( [int(strc) for strc in structure.split(",") ] ))

            HP_DROPOUT = hp.HParam('dropout', hp.Discrete(  [float(strc) for strc in optimaizer.split(",")] ))

            HP_OPTIMIZER = hp.HParam('optimizer', hp.Discrete(  [str(strc) for strc in optimaizer.split(",")]   ))

            HP_LEARNINGRATE=hp.HParam('leraning_rate', hp.Discrete( [float(strc) for strc in learing_rate.split(",")]  ) )

            HP_L2=hp.HParam('l2', hp.Discrete( [float(strc) for strc in regularitaion.split(",")]  ))

            HP_ACTIVATION=hp.HParam('activation', hp.Discrete(  [str(strc) for strc in activation.split(",")]   ))

            
            batch_sizes=int(batch_size)
            epoch=int(epochs)

            trying_model.init(HP_STRUCTURE,HP_DROPOUT,HP_OPTIMIZER,HP_LEARNINGRATE,HP_L2,HP_ACTIVATION,batch_sizes,epoch)



            os.system("sleep 5 && tensorboard --logdir "+log_dir+ "  & " )
            os.system("firefox http://localhost:6006/ & ")

            trying_model.lancer()

            logger.info("train Train_model ... OK ")
            


        except Exception as e:
            print(e)

            try : 
                self.lable_status.pack_forget()
                self.lable_status = Label(self.frame_right,text=language[60],fg="red", font=controller.font)
                self.lable_status.pack(side='top',expand=YES)

                METRIC_ACCURACY = 'accuracy'
                METRIC_LOSS='loss'
                log_dir='../logs/train/'

                HP_STRUCTURE= hp.HParam('structure_model', hp.Discrete([1]))
                HP_DROPOUT = hp.HParam('dropout', hp.Discrete([0.20]))
                HP_OPTIMIZER = hp.HParam('optimizer', hp.Discrete(['adam']))
                HP_LEARNINGRATE=hp.HParam('leraning_rate', hp.Discrete([0.001]))
                HP_MOMENTUM=hp.HParam('momentum', hp.Discrete([0.01]))
                HP_L2=hp.HParam('l2', hp.Discrete([0.001]))
                HP_ACTIVATION=hp.HParam('activation', hp.Discrete(['relu']))
                HP_AUGMENTATION=hp.HParam('data_augmentation',hp.Discrete(["true"]))
                
                batch_sizes=1024
                epoch=10

                trying_model.init(HP_STRUCTURE,HP_DROPOUT,HP_OPTIMIZER,HP_LEARNINGRATE,HP_L2,HP_ACTIVATION,batch_sizes,epoch)



                os.system("sleep 5 && tensorboard --logdir "+log_dir+ "  & " )
                os.system("firefox http://localhost:6006/ & ")

                trying_model.lancer()

                logger.info("train Train_model ... OK ")


            except Exception as e:
                logger.error("train Train_model ... KO ")
                logger.error(f"The error '{e}' occurred")

        logger.error("train Train_model ... KO ")



if __name__ == "__main__":

    app = SampleApp()
    app.mainloop()