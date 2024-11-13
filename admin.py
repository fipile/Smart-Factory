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
        self.back_btn = ctk.CTkButton(self, text="Voltar", width=100, fg_color='#772581',command= self.back, hover_color='black')
        self.back_btn.place(x=10, y=560)
        self.home_btn = ctk.CTkButton(self, text="Home", width=100, fg_color='#772581',command= self.home, hover_color='black')
        self.home_btn.place(x=10, y=10)
        self.prices_frame = ctk.CTkFrame(master=self, width=400, height=300, corner_radius=10, fg_color='white')
        self.prices_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        for row in range(5):
            self.prices_frame.grid_rowconfigure(row, weight=1)
        for col in range(3):
            self.prices_frame.grid_columnconfigure(col, weight=1)
        self.show_payment()


    
    def Labels(self):
        for widget in self.prices_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.prices_frame, text='260mL').grid(row=0, column=0, padx=20, pady=10)
        ctk.CTkLabel(self.prices_frame, text='350mL').grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkLabel(self.prices_frame, text='500mL').grid(row=2, column=0, padx=20, pady=10)
        ctk.CTkLabel(self.prices_frame, text='750mL').grid(row=3, column=0, padx=20, pady=10)
        ctk.CTkLabel(self.prices_frame, text='1L').grid(row=4, column=0, padx=20, pady=10)

    def fetch_prices(self, bebida):
        db = connect_db()
        cursor = db.cursor(dictionary=True)  # Use dictionary=True para acessar colunas pelo nome
        try:
            query = "SELECT * FROM prices WHERE nome = %s"
            cursor.execute(query, (bebida,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                return None
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao buscar preços: {err}")
        finally:
            cursor.close()
            db.close()

    def update_prices_in_db(self, bebida, novos_precos):
        db = connect_db()
        cursor = db.cursor()
        try:
            query = """
                UPDATE prices
                SET ml_260 = %s, ml_350 = %s, ml_500 = %s, ml_750 = %s, l_1 = %s
                WHERE nome = %s
            """
            values = (
                novos_precos.get('260mL'),
                novos_precos.get('350mL'),
                novos_precos.get('500mL'),
                novos_precos.get('750mL'),
                novos_precos.get('1L'),
                bebida,
            )
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Sucesso", "Preços atualizados com sucesso!")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao atualizar preços: {err}")
        finally:
            cursor.close()
            db.close()

    def show_payment(self):
        for widget in self.prices_frame.winfo_children():
            widget.destroy()
        
        self.individual_price = ctk.CTkButton(self.prices_frame, text="Preços Individuais", fg_color='#772581', hover_color='black', command= self.singlePrices)
        self.individual_price.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        self.package_price = ctk.CTkButton(self.prices_frame, text="Preço dos Engradados",  fg_color='#772581', hover_color='black')
        self.package_price.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
        self.orders_button = ctk.CTkButton(self.prices_frame, text="Perfis e Pedidos", fg_color='#772581', hover_color='black', command= lambda: self.orders)
        self.orders_button.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

    def singlePrices(self):
        for widget in self.prices_frame.winfo_children():
            widget.destroy()
        ctk.CTkButton(self.prices_frame, text="Skol:", command=self.skolprices).grid(row=0, column=0, padx=20, pady=10)
        ctk.CTkButton(self.prices_frame, text="Brahma:", command=self.brahmaprices).grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkButton(self.prices_frame, text="Heineken:", command=self.heinekenprices).grid(row=2, column=0, padx=20, pady=10)
        ctk.CTkButton(self.prices_frame, text="Antartica:", command=self.antarticaprices).grid(row=3, column=0, padx=20, pady=10)
    
    def skolprices(self):
        self.Labels()
        precos_atuais = self.fetch_prices('Skol')

        self.skol_price260 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.skol_price260.grid(row=0, column=1, padx=20, pady=10)
        self.skol_price260.insert(0, precos_atuais.get('ml_260', ''))  # Insere o preço atual

        self.skol_price350 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.skol_price350.grid(row=1, column=1, padx=20, pady=10)
        self.skol_price350.insert(0, precos_atuais.get('ml_350', ''))

        self.skol_price500 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.skol_price500.grid(row=2, column=1, padx=20, pady=10)
        self.skol_price500.insert(0, precos_atuais.get('ml_500', ''))

        self.skol_price750 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.skol_price750.grid(row=3, column=1, padx=20, pady=10)
        self.skol_price750.insert(0, precos_atuais.get('ml_750', ''))

        self.skol_price1L = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.skol_price1L.grid(row=4, column=1, padx=20, pady=10)
        self.skol_price1L.insert(0, precos_atuais.get('l_1', ''))

        # Botão para salvar os preços
        save_button = ctk.CTkButton(self.prices_frame, text="Salvar", command=self.save_skol_prices)
        save_button.grid(row=5, column=0, columnspan=2, pady=20)

    def save_skol_prices(self):
        novos_precos = {
            '260mL': self.skol_price260.get(),
            '350mL': self.skol_price350.get(),
            '500mL': self.skol_price500.get(),
            '750mL': self.skol_price750.get(),
            '1L': self.skol_price1L.get(),
        }
        self.update_prices_in_db('Skol', novos_precos)



    def brahmaprices(self):
        self.Labels()
        precos_atuais = self.fetch_prices('Brahma')

        self.brahma_price260 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.brahma_price260.grid(row=0, column=1, padx=20, pady=10)
        self.brahma_price260.insert(0, precos_atuais.get('ml_260', ''))

        self.brahma_price350 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.brahma_price350.grid(row=1, column=1, padx=20, pady=10)
        self.brahma_price350.insert(0, precos_atuais.get('ml_350', ''))

        self.brahma_price500 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.brahma_price500.grid(row=2, column=1, padx=20, pady=10)
        self.brahma_price500.insert(0, precos_atuais.get('ml_500', ''))

        self.brahma_price750 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.brahma_price750.grid(row=3, column=1, padx=20, pady=10)
        self.brahma_price750.insert(0, precos_atuais.get('ml_750', ''))

        self.brahma_price1L = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.brahma_price1L.grid(row=4, column=1, padx=20, pady=10)
        self.brahma_price1L.insert(0, precos_atuais.get('l_1', ''))

        save_button = ctk.CTkButton(self.prices_frame, text="Salvar", command=self.save_brahma_prices)
        save_button.grid(row=5, column=0, columnspan=2, pady=20)

    def save_brahma_prices(self):
        novos_precos = {
            '260mL': self.brahma_price260.get(),
            '350mL': self.brahma_price350.get(),
            '500mL': self.brahma_price500.get(),
            '750mL': self.brahma_price750.get(),
            '1L': self.brahma_price1L.get(),
        }
        self.update_prices_in_db('Brahma', novos_precos)

    def heinekenprices(self):
        self.Labels()
        precos_atuais = self.fetch_prices('Heineken')

        self.heineken_price260 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price260.grid(row=0, column=1, padx=20, pady=10)
        self.heineken_price260.insert(0, precos_atuais.get('ml_260', ''))

        self.heineken_price350 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price350.grid(row=1, column=1, padx=20, pady=10)
        self.heineken_price350.insert(0, precos_atuais.get('ml_350', ''))

        self.heineken_price500 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price500.grid(row=2, column=1, padx=20, pady=10)
        self.heineken_price500.insert(0, precos_atuais.get('ml_500', ''))

        self.heineken_price750 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price750.grid(row=3, column=1, padx=20, pady=10)
        self.heineken_price750.insert(0, precos_atuais.get('ml_750', ''))

        self.heineken_price1L = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price1L.grid(row=4, column=1, padx=20, pady=10)
        self.heineken_price1L.insert(0, precos_atuais.get('l_1', ''))

        save_button = ctk.CTkButton(self.prices_frame, text="Salvar", command=self.save_heineken_prices)
        save_button.grid(row=5, column=0, columnspan=2, pady=20)

    def save_heineken_prices(self):
        novos_precos = {
            '260mL': self.heineken_price260.get(),
            '350mL': self.heineken_price350.get(),
            '500mL': self.heineken_price500.get(),
            '750mL': self.heineken_price750.get(),
            '1L': self.heineken_price1L.get(),
        }
        self.update_prices_in_db('Heineken', novos_precos)

    def antarticaprices(self):
        self.Labels()
        precos_atuais = self.fetch_prices('Antartica')

        self.antartica_price260 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price260.grid(row=0, column=1, padx=20, pady=10)
        self.antartica_price260.insert(0, precos_atuais.get('ml_260', ''))

        self.antartica_price350 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price350.grid(row=1, column=1, padx=20, pady=10)
        self.antartica_price350.insert(0, precos_atuais.get('ml_350', ''))

        self.antartica_price500 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price500.grid(row=2, column=1, padx=20, pady=10)
        self.antartica_price500.insert(0, precos_atuais.get('ml_500', ''))

        self.antartica_price750 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price750.grid(row=3, column=1, padx=20, pady=10)
        self.antartica_price750.insert(0, precos_atuais.get('ml_750', ''))

        self.antartica_price1L = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price1L.grid(row=4, column=1, padx=20, pady=10)
        self.antartica_price1L.insert(0, precos_atuais.get('l_1', ''))

        save_button = ctk.CTkButton(self.prices_frame, text="Salvar", command=self.save_antarctica_prices)
        save_button.grid(row=5, column=0, columnspan=2, pady=20)

    def save_antarctica_prices(self):
        novos_precos = {
            '260mL': self.antartica_price260.get(),
            '350mL': self.antartica_price350.get(),
            '500mL': self.antartica_price500.get(),
            '750mL': self.antartica_price750.get(),
            '1L': self.antartica_price1L.get(),
        }
        self.update_prices_in_db('Antartica', novos_precos)
        
        
    def heinekenprices(self):
        self.Labels()
        precos_atuais = self.fetch_prices('Heineken')

        self.heineken_price260 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price260.grid(row=0, column=1, padx=20, pady=10)
        self.heineken_price260.insert(0, precos_atuais.get('ml_260', ''))

        self.heineken_price350 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price350.grid(row=1, column=1, padx=20, pady=10)
        self.heineken_price350.insert(0, precos_atuais.get('ml_350', ''))

        self.heineken_price500 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price500.grid(row=2, column=1, padx=20, pady=10)
        self.heineken_price500.insert(0, precos_atuais.get('ml_500', ''))

        self.heineken_price750 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price750.grid(row=3, column=1, padx=20, pady=10)
        self.heineken_price750.insert(0, precos_atuais.get('ml_750', ''))

        self.heineken_price1L = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price1L.grid(row=4, column=1, padx=20, pady=10)
        self.heineken_price1L.insert(0, precos_atuais.get('l_1', ''))

        save_button = ctk.CTkButton(self.prices_frame, text="Salvar", command=self.save_heineken_prices)
        save_button.grid(row=5, column=0, columnspan=2, pady=20)

    def save_heineken_prices(self):
        novos_precos = {
            '260mL': self.heineken_price260.get(),
            '350mL': self.heineken_price350.get(),
            '500mL': self.heineken_price500.get(),
            '750mL': self.heineken_price750.get(),
            '1L': self.heineken_price1L.get(),
        }
        self.update_prices_in_db('Heineken', novos_precos)

    def antarticaprices(self):
        self.Labels()
        precos_atuais = self.fetch_prices('Antartica')

        self.antartica_price260 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price260.grid(row=0, column=1, padx=20, pady=10)
        self.antartica_price260.insert(0, precos_atuais.get('ml_260', ''))

        self.antartica_price350 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price350.grid(row=1, column=1, padx=20, pady=10)
        self.antartica_price350.insert(0, precos_atuais.get('ml_350', ''))

        self.antartica_price500 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price500.grid(row=2, column=1, padx=20, pady=10)
        self.antartica_price500.insert(0, precos_atuais.get('ml_500', ''))

        self.antartica_price750 = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price750.grid(row=3, column=1, padx=20, pady=10)
        self.antartica_price750.insert(0, precos_atuais.get('ml_750', ''))

        self.antartica_price1L = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price1L.grid(row=4, column=1, padx=20, pady=10)
        self.antartica_price1L.insert(0, precos_atuais.get('l_1', ''))

        save_button = ctk.CTkButton(self.prices_frame, text="Salvar", command=self.save_antarctica_prices)
        save_button.grid(row=5, column=0, columnspan=2, pady=20)

    def save_antarctica_prices(self):
        novos_precos = {
            '260mL': self.antartica_price260.get(),
            '350mL': self.antartica_price350.get(),
            '500mL': self.antartica_price500.get(),
            '750mL': self.antartica_price750.get(),
            '1L': self.antartica_price1L.get(),
        }
        self.update_prices_in_db('Antartica', novos_precos)

    def LabelsEngradados(self):
        for widget in self.prices_frame.winfo_children():
            widget.destroy()
        ctk.CTkLabel(self.prices_frame, text='260mL (15 unidades)').grid(row=0, column=0, padx=20, pady=10)
        ctk.CTkLabel(self.prices_frame, text='350mL (15 unidades)').grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkLabel(self.prices_frame, text='500mL (15 unidades)').grid(row=2, column=0, padx=20, pady=10)
        ctk.CTkLabel(self.prices_frame, text='1L (12 unidades)').grid(row=3, column=0, padx=20, pady=10)

    def fetch_prices_pj(self, bebida):
        db = connect_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM pricespj WHERE nome = %s"
            cursor.execute(query, (bebida,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                return None
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao buscar preços: {err}")
        finally:
            cursor.close()
            db.close()

    def update_prices_pj_in_db(self, bebida, novos_precos):
        db = connect_db()
        cursor = db.cursor()
        try:
            query = """
                UPDATE pricespj
                SET ml_260 = %s, ml_350 = %s, ml_500 = %s, l_1 = %s
                WHERE nome = %s
            """
            values = (
                novos_precos.get('260mL'),
                novos_precos.get('350mL'),
                novos_precos.get('500mL'),
                novos_precos.get('1L'),
                bebida,
            )
            cursor.execute(query, values)
            db.commit()
            messagebox.showinfo("Sucesso", "Preços atualizados com sucesso!")
        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao atualizar preços: {err}")
        finally:
            cursor.close()
            db.close()

    def packagePrices(self):
        for widget in self.prices_frame.winfo_children():
            widget.destroy()
        ctk.CTkButton(self.prices_frame, text="Skol:", command=self.skolpricesEngradados).grid(row=0, column=0, padx=20, pady=10)
        ctk.CTkButton(self.prices_frame, text="Brahma:", command=self.brahmapricesEngradados).grid(row=1, column=0, padx=20, pady=10)
        ctk.CTkButton(self.prices_frame, text="Heineken:", command=self.heinekenpricesEngradados).grid(row=2, column=0, padx=20, pady=10)
        ctk.CTkButton(self.prices_frame, text="Antartica:", command=self.antarticapricesEngradados).grid(row=3, column=0, padx=20, pady=10)

    def skolpricesEngradados(self):
        self.LabelsEngradados()
        precos_atuais = self.fetch_prices_pj('Skol')

        self.skol_price260_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.skol_price260_engradado.grid(row=0, column=1, padx=20, pady=10)
        self.skol_price260_engradado.insert(0, precos_atuais.get('ml_260', ''))

        self.skol_price350_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.skol_price350_engradado.grid(row=1, column=1, padx=20, pady=10)
        self.skol_price350_engradado.insert(0, precos_atuais.get('ml_350', ''))

        self.skol_price500_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.skol_price500_engradado.grid(row=2, column=1, padx=20, pady=10)
        self.skol_price500_engradado.insert(0, precos_atuais.get('ml_500', ''))

        self.skol_price1L_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.skol_price1L_engradado.grid(row=3, column=1, padx=20, pady=10)
        self.skol_price1L_engradado.insert(0, precos_atuais.get('l_1', ''))

        save_button = ctk.CTkButton(self.prices_frame, text="Salvar", command=self.save_skol_prices_engradado)
        save_button.grid(row=4, column=0, columnspan=2, pady=20)

    def save_skol_prices_engradado(self):
        novos_precos = {
            '260mL': self.skol_price260_engradado.get(),
            '350mL': self.skol_price350_engradado.get(),
            '500mL': self.skol_price500_engradado.get(),
            '1L': self.skol_price1L_engradado.get(),
        }
        self.update_prices_pj_in_db('Skol', novos_precos)

    def brahmapricesEngradados(self):
        self.LabelsEngradados()
        precos_atuais = self.fetch_prices_pj('Brahma')

        self.brahma_price260_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.brahma_price260_engradado.grid(row=0, column=1, padx=20, pady=10)
        self.brahma_price260_engradado.insert(0, precos_atuais.get('ml_260', ''))

        self.brahma_price350_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.brahma_price350_engradado.grid(row=1, column=1, padx=20, pady=10)
        self.brahma_price350_engradado.insert(0, precos_atuais.get('ml_350', ''))

        self.brahma_price500_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.brahma_price500_engradado.grid(row=2, column=1, padx=20, pady=10)
        self.brahma_price500_engradado.insert(0, precos_atuais.get('ml_500', ''))

        self.brahma_price1L_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.brahma_price1L_engradado.grid(row=3, column=1, padx=20, pady=10)
        self.brahma_price1L_engradado.insert(0, precos_atuais.get('l_1', ''))

        save_button = ctk.CTkButton(self.prices_frame, text="Salvar", command=self.save_brahma_prices_engradado)
        save_button.grid(row=4, column=0, columnspan=2, pady=20)

    def save_brahma_prices_engradado(self):
        novos_precos = {
            '260mL': self.brahma_price260_engradado.get(),
            '350mL': self.brahma_price350_engradado.get(),
            '500mL': self.brahma_price500_engradado.get(),
            '1L': self.brahma_price1L_engradado.get(),
        }
        self.update_prices_pj_in_db('Brahma', novos_precos)

    def heinekenpricesEngradados(self):
        self.LabelsEngradados()
        precos_atuais = self.fetch_prices_pj('Heineken')

        self.heineken_price260_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price260_engradado.grid(row=0, column=1, padx=20, pady=10)
        self.heineken_price260_engradado.insert(0, precos_atuais.get('ml_260', ''))

        self.heineken_price350_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price350_engradado.grid(row=1, column=1, padx=20, pady=10)
        self.heineken_price350_engradado.insert(0, precos_atuais.get('ml_350', ''))

        self.heineken_price500_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price500_engradado.grid(row=2, column=1, padx=20, pady=10)
        self.heineken_price500_engradado.insert(0, precos_atuais.get('ml_500', ''))

        self.heineken_price1L_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.heineken_price1L_engradado.grid(row=3, column=1, padx=20, pady=10)
        self.heineken_price1L_engradado.insert(0, precos_atuais.get('l_1', ''))

        save_button = ctk.CTkButton(self.prices_frame, text="Salvar", command=self.save_heineken_prices_engradado)
        save_button.grid(row=4, column=0, columnspan=2, pady=20)

    def save_heineken_prices_engradado(self):
        novos_precos = {
            '260mL': self.heineken_price260_engradado.get(),
            '350mL': self.heineken_price350_engradado.get(),
            '500mL': self.heineken_price500_engradado.get(),
            '1L': self.heineken_price1L_engradado.get(),
        }
        self.update_prices_pj_in_db('Heineken', novos_precos)

    def antarticapricesEngradados(self):
        self.LabelsEngradados()
        precos_atuais = self.fetch_prices_pj('Antartica')

        self.antartica_price260_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price260_engradado.grid(row=0, column=1, padx=20, pady=10)
        self.antartica_price260_engradado.insert(0, precos_atuais.get('ml_260', ''))

        self.antartica_price350_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price350_engradado.grid(row=1, column=1, padx=20, pady=10)
        self.antartica_price350_engradado.insert(0, precos_atuais.get('ml_350', ''))

        self.antartica_price500_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price500_engradado.grid(row=2, column=1, padx=20, pady=10)
        self.antartica_price500_engradado.insert(0, precos_atuais.get('ml_500', ''))

        self.antartica_price1L_engradado = ctk.CTkEntry(self.prices_frame, width=60, font=('Century Gothic bold', 16), fg_color='transparent')
        self.antartica_price1L_engradado.grid(row=3, column=1, padx=20, pady=10)
        self.antartica_price1L_engradado.insert(0, precos_atuais.get('l_1', ''))

        save_button = ctk.CTkButton(self.prices_frame, text="Salvar", command=self.save_antarctica_prices_engradado)
        save_button.grid(row=4, column=0, columnspan=2, pady=20)

    def save_antarctica_prices_engradado(self):
        novos_precos = {
            '260mL': self.antartica_price260_engradado.get(),
            '350mL': self.antartica_price350_engradado.get(),
            '500mL': self.antartica_price500_engradado.get(),
            '1L': self.antartica_price1L_engradado.get(),
        }
        self.update_prices_pj_in_db('Antartica', novos_precos)

    def show_payment(self):
        for widget in self.prices_frame.winfo_children():
            widget.destroy()
        
        self.individual_price = ctk.CTkButton(self.prices_frame, text="Preços Individuais", fg_color='#772581', hover_color='black', command= self.singlePrices)
        self.individual_price.grid(row=0, column=0, pady=20, padx=20, sticky="ew")
        self.package_price = ctk.CTkButton(self.prices_frame, text="Preço dos Engradados",  fg_color='#772581', hover_color='black', command=self.packagePrices)
        self.package_price.grid(row=1, column=0, pady=10, padx=20, sticky="ew")
        self.orders_button = ctk.CTkButton(self.prices_frame, text="Perfis e Pedidos", fg_color='#772581', hover_color='black', command= self.orders)
        self.orders_button.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

    def back(self):
        self.destroy()
        subprocess.run(['python', 'admin.py'])

    def home(self):
        self.destroy()
        subprocess.run(['python', 'adminlogin.py'])

    def orders(self):
        self.destroy()
        subprocess.run(['python', 'orders.py'])


        

            

            

        



if __name__ == "__main__":
    app = App()
    app.mainloop()


