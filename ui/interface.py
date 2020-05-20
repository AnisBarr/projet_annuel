
#import statements
from tkinter import *
import tkinter  as tk
import tkinter.font as tkFont
from PIL import ImageTk,Image
import time


class PageTwo(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="This is page 2")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page")
        button.pack()

window = Tk()
window.title("Sign Language Translator")
window.geometry("833x636")
window.minsize(833,636)
# window.maxsize(833,636)
# window.config(background='#fdfdfd')

menu =  Menu(window)
window.config(menu=menu)
file = Menu(menu,tearoff=0)
file.add_command(label="exit",command= window.quit)
compte = Menu(menu,tearoff=0)
compte.add_command(label="conection",command= window.quit)
compte.add_command(label="deconection",command= window.quit)
compte.add_command(label="modifier mots de passe",command= window.quit)
compte.add_command(label="suprimer compte",command= window.quit)
menu.add_cascade(label="Fichier" , menu =file)
menu.add_cascade(label="Compte" , menu =compte)
        



first_frame = Frame(window)
first_frame.pack(fill=BOTH, expand=YES)
canvas = Canvas(first_frame, height=636, width=833)
filename = PhotoImage(file = "../resources/dd.png")
canvas.create_image(0,0,anchor=NW,image=filename)

canvas.pack()

canvas.pack(expand=YES)

font = tkFont.Font(family="Helvetica",size=15,weight = 'bold')


fm = PageTwo(window)

button = Button(first_frame, text="Conection" , font =font,command=fm.tkraise())
button_2 = Button(first_frame, text="Utiliser sans Conection" ,font =font)
button_window = canvas.create_window(210, 540, anchor=NW, window=button)
button_window = canvas.create_window(410, 540, anchor=NW, window=button_2)



window.mainloop()


