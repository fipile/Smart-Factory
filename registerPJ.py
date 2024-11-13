import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import main
import styles
import mysql.connector
import subprocess
import sys
import random
import string
from tkinter import messagebox

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="!",  
        database="testdb"
    )





class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.layout_config()
        self.configure(fg_color="#312581")
        self.system()

    def layout_config(self):
        self.title('Smart Factory')
        self.geometry("800x600+100+50")
        self.resizable(width= False, height= False)

    def system(self):
        self.btn_back = ctk.CTkButton(self, text="Voltar", width=200, fg_color='#772581',command= self.back, hover_color='black')
        self.btn_back.place(x=10, y=560)
        frame = ctk.CTkFrame(master=self, width=400, height=700, corner_radius=10, fg_color='white')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        for row in range(4):
            frame.grid_rowconfigure(row, weight=1)
        for col in range(2):
            frame.grid_columnconfigure(col, weight=1)
        self.entry_username = ctk.CTkEntry(master=frame, width=200, font=('Century Gothic bold', 16), fg_color='transparent')
        self.entry_username.grid(row=0, column=0, sticky="ew", padx=20, pady=(60, 0))
        self.entry_email = ctk.CTkEntry(master=frame, width=200, font=('Century Gothic bold', 16), fg_color='transparent')
        self.entry_email.grid(row=1, column=0, sticky="ew", padx=20, pady=(60, 0))
        self.entry_password = ctk.CTkEntry(master=frame, width=200, show='*', font=('Century Gothic bold', 16), fg_color='transparent' )
        self.entry_password.grid(row=0, column=1, sticky="ew", padx=20, pady=(60, 0))
        self.entry_cnpj = ctk.CTkEntry(master=frame, width=200, font=('Century Gothic bold', 16), fg_color='transparent')
        self.entry_cnpj.grid(row=1, column=1, sticky="ew", padx=20, pady=(60, 0))
        styles.registerBtnPJ(self, frame)


        lb_username = ctk.CTkLabel(master=frame, text='Usuario', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])
        lb_username.grid(row=0, column=0, sticky="", padx=20)
        lb_email = ctk.CTkLabel(master=frame, text='Email', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])  
        lb_email.grid(row=1, column=0, sticky="", padx=20)
        lb_password = ctk.CTkLabel(master=frame, text='Senha', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])
        lb_password.grid(row=0, column=1, sticky="", padx=20)
        lb_cnpj = ctk.CTkLabel(master=frame, text='CNPJ', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])
        lb_cnpj.grid(row=1, column=1, padx=(20))

         



    def back(self):
        self.destroy()
        subprocess.run(['python', 'LoginPJ.py'])

    def Register(self):
        username = self.entry_username.get().lower()
        email = self.entry_email.get()
        password = self.entry_password.get()
        cnpj = self.entry_cnpj.get()

        
        if username == "" or password == "" or email == "" or cnpj =="":
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return

        
        db = connect_db()
        cursor = db.cursor(prepared=True)
        try:
            query_check = "SELECT 1 FROM userpj WHERE email = %s"
            cursor.execute(query_check, (email,))
            email_exists = cursor.fetchone() is not None

            query_check_username = "SELECT 1 FROM userpj WHERE username = %s"
            cursor.execute(query_check_username, (username,))
            username_exists = cursor.fetchone() is not None

            query_check_cnpj = "SELECT 1 FROM userpj WHERE cnpj = %s"
            cursor.execute(query_check_cnpj, (cnpj,))
            cnpj_exists = cursor.fetchone() is not None

            if cnpj_exists:
                messagebox.showerror("Erro", "Já existe um usuário com este CNPJ!")


            if email_exists:
                messagebox.showerror("Erro", "Já existe um usuário com este email!")

            elif username_exists:
                messagebox.showerror("Erro", "Já existe um usuário com este nome de usuário")
            
            else:
                query = "INSERT INTO userpj (username, password, email, cnpj, userType) VALUES (%s, %s, %s, %s, 'PJ')"
                cursor.execute(query, (username, password, email, cnpj))
                db.commit()
                messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
                self.destroy()
                subprocess.run(['python', 'LoginPJ.py', username])
        except mysql.connector.Error as err:
            messagebox.showerror("Erro",  f"Ocorreu um erro: {err}")
        finally:
            db.close()



    def change_apm(self, nova_aparencia):
        ctk.set_appearance_mode(nova_aparencia)

if __name__ == "__main__":
    app = App()
    app.mainloop()  