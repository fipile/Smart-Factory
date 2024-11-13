import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import styles
import mysql.connector 
import subprocess
import sys
import random
import string
#Licor Express
#Sistema de vendas de uma smart factory de bebidas
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configure(fg_color="#312581")
        self.layout_config()
        self.system()
#place(x=10, y=560

    def layout_config(self):
        self.title('Smart Factory')
        self.geometry("800x600+100+50")
        self.resizable(width= False, height= False)

    def system(self):
        styles.btn_PF(self)
        styles.btn_PJ(self)
        btn_admin = ctk.CTkButton(self, text="Login como Admnistrador", width=200, fg_color='#772581',command=self.adminLogin, hover_color='black')
        btn_admin.place(x = 600,  y = 550)

    def loginPF(self):
        self.destroy()
        subprocess.run(['python', 'loginPF.py'])
    
    def loginPJ(self):
        self.destroy()
        subprocess.run(['python', 'loginPJ.py'])
    def adminLogin(self):
        self.destroy()
        subprocess.run(['python', 'adminlogin.py'])





    def change_apm(self, nova_aparencia):
        ctk.set_appearance_mode(nova_aparencia)

if __name__ == "__main__":
    app = App()
    app.mainloop()