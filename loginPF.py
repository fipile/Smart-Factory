import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import main
import styles
import subprocess
import mysql.connector
import emailtext
from sender import send_email
from tkinter import messagebox
import sys

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
        self.login_attempts = 0
         
    def layout_config(self):
        self.title('Smart Factory')
        self.geometry("800x600+100+50")
        self.resizable(width= False, height= False)

    def system(self):
        self.btn_back = ctk.CTkButton(self, text="Voltar", width=200, fg_color='#772581',command= self.back, hover_color='black')
        self.btn_back.place(x=10, y=560)
        frame = ctk.CTkFrame(master=self, width=400, height=300, corner_radius=10, fg_color='white')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        for row in range(4):
            frame.grid_rowconfigure(row, weight=1)
        for col in range(2):
            frame.grid_columnconfigure(col, weight=1)
        self.entry_username = ctk.CTkEntry(master=frame, width=200, font=('Century Gothic bold', 16), fg_color='transparent')
        self.entry_username.grid(row=0, column=0, sticky="ew", padx=20, pady=(60, 0))
        self.entry_password = ctk.CTkEntry(master=frame, width=200, show='*', font=('Century Gothic bold', 16), fg_color='transparent' )
        self.entry_password.grid(row=1, column=0, sticky="ew", padx=20, pady=(60, 0))
        lb_username = ctk.CTkLabel(master=frame, text='usuario', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])
        lb_username.grid(row=0, column=0, sticky="w", padx=20)    
        lb_password = ctk.CTkLabel(master=frame, text='senha', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])
        lb_password.grid(row=1, column=0, sticky="w", padx=20)   
        btn_login = ctk.CTkButton(frame, text ='Login', width=100, fg_color='#772581',command= lambda:self.Login(), hover_color='black')
        btn_login.grid(row=2, column=0, pady=(20, 10))
        btn_register = ctk.CTkButton(frame, text ='Registro', width=100, fg_color='#772581',command= lambda: self.register(), hover_color='black')
        btn_register.grid(row=3, column=0, pady=(10, 20))
        self.btn_forget = ctk.CTkButton(frame, text='Esqueci minha senha', fg_color='white', text_color='#0000EE',
                                       hover_color='lightgray', command=self.forget_password, width=200)
        self.btn_forget.grid(row=4, column=0, pady=(10, 20))
        

    def register(self):
        self.destroy()
        subprocess.run(['python', 'registerPF.py'])

    def forget_password(self):
        self.destroy()
        subprocess.run(['python', 'forget.py'])

    def Login(self):
        usernames = self.entry_username.get()
        password = self.entry_password.get()
        if usernames == "" or password == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return
        
        if usernames == "" or password == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return

    
        db = connect_db()
        cursor = db.cursor(prepared=True)

        query = "SELECT * FROM users WHERE usernames = %s AND password = %s"
        cursor.execute(query, (usernames, password))
        user_name = cursor.fetchone()
        if user_name:
            self.username = user_name[1]
            messagebox.showinfo("Sucesso", "Login bem-sucedido!")
            self.destroy()
            subprocess.run(['python', 'clientprices.py', self.username])
            self.login_attempts = 0  # Reset attempts on successful login
        else:
            self.login_attempts += 1
            if self.login_attempts >= 3:
                # Reset password after 3 failed attempts
                self.reset_password(usernames)
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos!")

        cursor.close()
        db.close()
    def reset_password(self, usernames):
        db = connect_db()
        cursor = db.cursor(prepared=True)

        new_password = emailtext.random_number_string(6)  # Get random password
        try:
            query = "UPDATE users SET password = %s WHERE usernames = %s"
            cursor.execute(query, (new_password, usernames))
            db.commit()

            # Send email with new password
            user_email = self.get_user_email(usernames)  # Get user's email
            message = emailtext.security_password(user_email)
            send_email(
                sender_email="smartfactoryltda@gmail.com",
                sender_password="ygtp tguv ztrh qoed",
                recipient_email=user_email,
                subject="Segurança da sua conta",
                message=message
            )

            messagebox.showinfo("Senha Redefinida", f"Tentativas permitidas excedidas, sua senha foi redefinida e enviada para seu email")
            self.login_attempts = 0  # Reset attempts after password reset
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao redefinir senha: {e}")
        finally:
            cursor.close()
            db.close()

    def get_user_email(self, usernames):
        db = connect_db()
        cursor = db.cursor(prepared=True)
        query = "SELECT email FROM users WHERE usernames = %s"
        cursor.execute(query, (usernames,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result[0] if result else None
    def get_current_user_id(self):
        return self.current_user_id
    
    def prices(self):
        self.destroy()
        subprocess.run(['python', 'clientprices.py'])

        
    def back(self):
        self.destroy()
        subprocess.run(['python', 'main.py'])

    def change_apm(self, nova_aparencia):
        ctk.set_appearance_mode(nova_aparencia)

if __name__ == "__main__":
    app = App()
    app.mainloop()