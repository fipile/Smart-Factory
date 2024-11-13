import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import emailtext
from sender import send_email


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
        self.forgetEmail()

    def layout_config(self):
        self.title('Smart Factory')
        self.geometry("400x400+100+50")
    
    
    def forgetEmail(self):
        lb_userEmail = ctk.CTkLabel(self, text='Digite seu email de usuário', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])
        lb_userEmail.place(x=100, y=120)
        self.entry_userEmail = ctk.CTkEntry(self, width=200, font=('Century Gothic bold', 16), fg_color='transparent')
        self.entry_userEmail.place(x=100, y=150)

        self.btn_email = ctk.CTkButton(self, text='Enviar para o email', fg_color='#151', command=self.IdInput, hover_color='#131') 
        self.btn_email.place(x=100, y = 190)

        self.entry_code = ctk.CTkEntry(self, width=100, font= ('Century Gothic bold', 16), fg_color='transparent')
        self.entry_code.place(x= 100, y= 250)
        self.btn_code = ctk.CTkButton(self, text='Insira o código recebido', fg_color='#151', command=self.CodeEntry, hover_color='#131') 
        self.btn_code.place(x=100, y = 290)
        
        self.btn_back = ctk.CTkButton(self, text='Voltar', fg_color='#151', command=self.back, hover_color='#131', width=100) 
        self.btn_back.place(x=10, y = 30)

    def back(self):
        self.destroy()
        subprocess.run(['python', 'main.py'])


    def IdInput(self):
        userMail = self.entry_userEmail.get()
        if userMail == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return
        try:

            message = emailtext.generate_email_text(userMail)
            send_email(
                sender_email="smartfactoryltda@gmail.com",  # Replace with your email
                sender_password="ygtp tguv ztrh qoed",      # Replace with your password
                recipient_email=userMail,  # Pass the user's email here
                subject="Recuperação de Senha",
                message= message
            )
            messagebox.showinfo("Sucesso", "Email enviado com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao enviar email: {e}")
        
    def CodeEntry(self):
        userCode = self.entry_code.get()
        userMail = self.entry_userEmail.get()
        if userCode == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return
        if userCode == emailtext.random_string:
            self.destroy()
            subprocess.run(['python', 'newpassword.py', userMail])
        

        
    

    def change_apm(self, nova_aparencia):
        ctk.set_appearance_mode(nova_aparencia)

if __name__ == "__main__":
    app = App()
    app.mainloop()