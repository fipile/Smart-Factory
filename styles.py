import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
from customtkinter import *
import main
import loginPJ
import loginPF
import subprocess
import registerPF
import registerPJ
import clientprices
import mysql.connector
import cart

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="!",  
        database="testdb"
    )

def btn_PJ(self):
    imagePJ = Image.open("ParaPJ.png")
    imagePJ= ctk.CTkImage(light_image=imagePJ, size=(200,200))
    image_lbl = ctk.CTkLabel(self, image=imagePJ, text="")
    image_lbl.place(x = 450, y = 200)
    btnPF = ctk.CTkButton(self, text="Empresas", width=100, fg_color='#772581',command= lambda: main.App.loginPJ(self),  hover_color='black')
    btnPF.place(x= 500, y = 360)
    
def btn_PF(self):
    imagePF = Image.open("ParaPF.png")
    imagePF = ctk.CTkImage(light_image=imagePF, size=(100,100))
    image_lbl = ctk.CTkLabel(self, image=imagePF, text="")
    image_lbl.place(x = 250, y = 250)
    btnPF = ctk.CTkButton(self, text="Pessoa Física", width=100, fg_color='#772581',command= lambda: main.App.loginPF(self), hover_color='black')
    btnPF.place(x= 250, y = 360)

def loginForPF(self):
    title = ctk.CTkLabel(self, text='Login e Registro', font=('Century Gothic bold', 20), text_color=["#fff", '#fff']).place(x=335, y=10) 

def loginForPJ(self):
    title = ctk.CTkLabel(self, text='Login e Registro', font=('Century Gothic bold', 20), text_color=["#fff", '#fff']).place(x=335, y=10)

def registerBtnPF(self, frame):
   btn_register = ctk.CTkButton(frame, text ='Registro', width=100, fg_color='#772581',command= lambda: registerPF.App.Register(self), hover_color='black')
   btn_register.grid(row=1, column=1, pady=(60,10))

def registerBtnPJ(self, frame):
    btn_register = ctk.CTkButton(frame, text ='Registro', width=100, fg_color='#772581',command= lambda: registerPJ.App.Register(self), hover_color='black')
    btn_register.grid(row=2, column=0, columnspan=2, pady=(60,10))

def adminLogin(self):
    title = ctk.CTkLabel(self, text='Login como Administrador', font=('Century Gothic bold', 20), text_color=["#fff", '#fff']).place(x=335, y=10) 

def Beverages(self, frame):
    img_skol = Image.open("Skol.png")
    img_heineken = Image.open("Heineken.png")
    img_antartica = Image.open("Antartica.png")
    img_brahma = Image.open("Brahma.png")
    img_skol = ctk.CTkImage(light_image=img_skol, size=(200,200))
    img_heineken = ctk.CTkImage(light_image=img_heineken, size=(200,200))
    img_antartica = ctk.CTkImage(light_image=img_antartica, size=(200,200))
    img_brahma = ctk.CTkImage(light_image=img_brahma, size=(200,200))
    skol_lb = ctk.CTkLabel(frame, image=img_skol, text="")
    skol_lb.grid(row=0, column=0, padx=10, pady=(20,0))
    heineken_lb = ctk.CTkLabel(frame, image=img_heineken, text="")
    heineken_lb.grid(row=0, column=1, padx=10, pady=40)
    antartica_lb = ctk.CTkLabel(frame, image=img_antartica, text="")
    antartica_lb.grid(row=1, column=0, padx=10, pady=10)
    brahma_lb = ctk.CTkLabel(frame, image=img_brahma, text="")
    brahma_lb.grid(row=1, column=1, padx=10, pady=10)
    title_skol = ctk.CTkLabel(frame, text='Skol', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])
    title_skol.grid(row=0, column=0, padx=10, pady=(0,60), sticky="n")
    title_heineken = ctk.CTkLabel(frame, text='Heineken', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])
    title_heineken.grid(row=0, column=1, padx=10, pady=(0,90), sticky="n")
    title_antartica = ctk.CTkLabel(frame, text='Antartica', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])
    title_antartica.grid(row=1, column=0, padx=10, pady=(0,80), sticky="n")
    title_brahma = ctk.CTkLabel(frame, text='Brahma', font=('Century Gothic bold', 16), text_color=["#000", '#fff'])
    title_brahma.grid(row=1, column=1, padx=10, pady=(0,80), sticky="n")

    plus_btn = ctk.CTkButton(self, text="Carrinho", fg_color='#772581',command= lambda: clientprices.App.Cart(self), width=100)
    plus_btn.place(x= 650, y= 500)

def CartFunctions(self):
    btn_clearcart = ctk.CTkButton(self, text ='Esvaziar Carrinho', width=100, fg_color='#772581', hover_color='black', command= lambda: cart.App.clear_cart(self))
    btn_clearcart.place(x=600,y = 500)
    btn_paycart = ctk.CTkButton(self, text ='Pagamento', width=100, fg_color='#772581', hover_color='black')
    btn_paycart.place(x=600,y = 450)


def fetch_prices_PF():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    prices = {}
    try:
        query = "SELECT * FROM prices"
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            bebida = row['nome']
            prices[bebida] = {
                '': '',
                '260mL': row['ml_260'],
                '350mL': row['ml_350'],
                '500mL': row['ml_500'],
                '750mL': row['ml_750'],
                '1L': row['l_1']
            }
        return prices

    except mysql.connector.Error as err:
        print(f"Erro ao buscar preços do banco de dados: {err}")
        return {}
    finally:
        cursor.close()
        db.close()

pricesPF = fetch_prices_PF()

def fetch_prices_PJ():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    prices = {}
    try:
        query = "SELECT * FROM pricespj"
        cursor.execute(query)
        results = cursor.fetchall()

        for row in results:
            bebida = row['nome']
            prices[bebida] = {
                '': '',
                '260mLx15 Unidades': row['ml_260'],
                '350mLx15 Unidades': row['ml_350'],
                '500mLx15 Unidades': row['ml_500'],
                '1Lx12 Unidades': row['l_1']
            }
        return prices

    except mysql.connector.Error as err:
        print(f"Erro ao buscar preços do banco de dados: {err}")
        return {} 
    finally:
        cursor.close()
        db.close()

pricesPJ = fetch_prices_PJ()




'''
pricesPF = {
            'Skol': {
                '': '',
                '260mL': 3.50,
                '350mL': 3.79,
                '500mL': 4.89,
                '750mL': 7.50,
                '1L' : 9.79,
                }, 
            'Heineken': {
                '': '',
                '260mL': 3.69,
                '350mL': 4.89,
                '500mL': 10.00,
                '750mL': 14.99,
                '1L' : 17.90,
                },
            'Antartica': {
                '': '',
                '260mL': 2.79,
                '350mL': 3.29,
                '500mL': 7.76,
                '750mL': 25,
                '1L' : 9.79,
            },
            'Brahma': {
                '': '',
                '260mL': 10,
                '350mL': 15,
                '500mL': 20,
                '750mL': 25,
                '1L' : 9.79,
            }
        }
'''




#U+002B
# U+2212











