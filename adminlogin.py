import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import main
import styles
import mysql.connector
import subprocess

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.configure(fg_color="#312581")
        self.layout_config()
        self.system()
         
    def layout_config(self):
        self.title('Smart Factory')
        self.geometry("800x600+100+50")
        self.resizable(width= False, height= False)

    def system(self):
        styles.adminLogin(self)
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
        btn_login = ctk.CTkButton(frame, text ='Login', width=100, fg_color='#772581',command= lambda:self.admin(), hover_color='black')
        btn_login.grid(row=2, column=0, pady=(20, 10))

    def back(self):
        self.destroy()
        subprocess.run(['python', 'main.py'])

    def admin(self):
        self.destroy()
        subprocess.run(['python', 'admin.py'])


def change_apm(self, nova_aparencia):
        ctk.set_appearance_mode(nova_aparencia)

if __name__ == "__main__":
    app = App()
    app.mainloop() 