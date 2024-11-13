import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
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
        self.passwordUpdate()
        self.user_email = sys.argv[1] if len(sys.argv) > 1 else None


    def layout_config(self):
        self.title('Smart Factory')
        self.geometry("400x400+100+50")
        self.resizable(width= False, height= False)


    def passwordUpdate(self):
        self.lb_NewPwd = ctk.CTkLabel(self, text='Digite a sua nova senha', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])
        self.lb_NewPwd.place(x=100, y=100)

        self.entry_NewPwd = ctk.CTkEntry(self, width=200,show='*', font=('Century Gothic bold', 16), fg_color='transparent')
        self.entry_NewPwd.place(x=100, y=150)

        self.lb_ConfirmPwd = ctk.CTkLabel(self, text='Confirme novamente sua senha', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])
        self.lb_ConfirmPwd.place(x=100, y=200)

        self.entry_ConfirmPwd = ctk.CTkEntry(self, width=200,show='*', font=('Century Gothic bold', 16), fg_color='transparent')
        self.entry_ConfirmPwd.place(x=100, y=250)

        self.btn_ResetPwd = ctk.CTkButton(self, text='Redefina sua senha', fg_color='#151', command=self.reset, hover_color='#131') 
        self.btn_ResetPwd.place(x=100, y = 300)

        self.btn_back = ctk.CTkButton(self, text='Voltar', fg_color='#151', command=self.back, hover_color='#131', width=100) 
        self.btn_back.place(x=10, y = 30)

    def reset(self):
        email = self.user_email
        newPwd = self.entry_NewPwd.get()
        confirmPwd = self.entry_ConfirmPwd.get()

        if newPwd == "" or confirmPwd == "":
            messagebox.showwarning("Aviso", "Preencha todos os campos")
            return
        
        if newPwd != confirmPwd:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
        
        try:
            db = connect_db()
            cursor = db.cursor(prepared=True)

            # Determine user type (PF or PJ) based on email
            cursor.execute("SELECT usernames FROM users WHERE email = %s", (email,))
            user_result = cursor.fetchone()
            cursor.execute("SELECT username FROM userpj WHERE email = %s", (email,))
            userpj_result = cursor.fetchone()

            if user_result:
                # User is PF, update 'users' table
                query = "UPDATE users SET password = %s WHERE email = %s"
            elif userpj_result:
                # User is PJ, update 'userpj' table
                query = "UPDATE userpj SET password = %s WHERE email = %s"
            else:
                messagebox.showerror("Erro", "Usuário não encontrado!")
                return

            cursor.execute(query, (newPwd, email))
            db.commit()
            cursor.close()
            db.close()
            messagebox.showinfo("Sucesso", "Sua senha foi redefinida com sucesso!")
            self.destroy()
            subprocess.run(['python', 'main.py'])

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao redefinir senha: {err}")
        finally:
            db.close()

        




    def back(self):
        self.destroy()
        subprocess.run(['python', 'forget.py'])


    def change_apm(self, nova_aparencia):
        ctk.set_appearance_mode(nova_aparencia)
if __name__ == "__main__":
    app = App()
    app.mainloop()
