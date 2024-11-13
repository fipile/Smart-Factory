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
        self.configure(fg_color="#312581")
        self.layout_config()
        self.username = "" 
        self.get_username()
        self.system()


    def layout_config(self):
        self.title('Smart Factory')
        self.geometry("800x600+100+50")
        self.resizable(width= False, height= False)
        

    def system(self):
        
        self.values=['','260mL','350mL','500mL','750mL', '1L']
        
        self.prices = styles.pricesPF

        
        self.back_btn = ctk.CTkButton(self, text="Voltar", width=100, fg_color='#772581',command= self.back, hover_color='black')
        self.back_btn.place(x=10, y=560)
        frame = ctk.CTkFrame(master=self, width=600, height=400, corner_radius=10, fg_color='white')
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        for row in range(4):
            frame.grid_rowconfigure(row, weight=1)
        for col in range(2):
            frame.grid_columnconfigure(col, weight=1)
        styles.Beverages(self, frame)
        self.skol_size = ctk.CTkOptionMenu(frame,fg_color='#772581', values=self.values, command= lambda event : self.update_price())
        self.skol_size.grid(row=0, column=0,padx=(0,20), pady=(210,0), sticky='s')
        self.entry_skolQuantity = ctk.CTkEntry(frame, width=30, font=('Century Gothic bold', 16), fg_color='transparent')
        self.entry_skolQuantity.grid(row = 0, column = 0, padx = (0,20),  sticky = "se" )
        self.heineken_size = ctk.CTkOptionMenu(frame,fg_color='#772581', values=self.values, command= lambda event : self.update_price())
        self.heineken_size.grid(row=0, column=1, padx=(0, 20), pady=(210,0), sticky='s')
        self.entry_heinekenQuantity = ctk.CTkEntry(frame, width=30, font=('Century Gothic bold', 16), fg_color='transparent')
        self.entry_heinekenQuantity.grid(row = 0, column = 1, padx = (0,20),  sticky = "se" )
        self.antartica_size = ctk.CTkOptionMenu(frame,fg_color='#772581',  values=self.values, command= lambda event : self.update_price())
        self.antartica_size.grid(row=1, column=0, padx=20, pady=(220,20), sticky='s')
        self.entry_antarticaQuantity = ctk.CTkEntry(frame, width=30, font=('Century Gothic bold', 16), fg_color='transparent')
        self.entry_antarticaQuantity.grid(row = 1, column = 0,  pady=(0,20), padx = (0,10),  sticky = "se" )
        self.brahma_size = ctk.CTkOptionMenu(frame,fg_color='#772581', values=self.values, command= lambda event : self.update_price())
        self.brahma_size.grid(row=1, column=1, padx=(0,20), pady=(220,20), sticky='s')
        self.entry_brahmaQuantity = ctk.CTkEntry(frame, width=30, font=('Century Gothic bold', 16), fg_color='transparent')
        self.entry_brahmaQuantity.grid(row = 1, column = 1, padx = (0,20), pady=(0,20),  sticky = "se" )
        self.skol_lb = ctk.CTkLabel(frame, text='')
        self.skol_lb.grid(row = 0, column = 0, padx = (0,20),  sticky = "e" )
        self.heineken_lb = ctk.CTkLabel(frame, text='')
        self.heineken_lb.grid(row = 0, column = 1, padx = (0,20),  sticky = "e" )
        self.antartica_lb = ctk.CTkLabel(frame, text='')
        self.antartica_lb.grid(row = 1, column = 0, padx = (0,20),  sticky = "e" )
        self.brahma_lb = ctk.CTkLabel(frame, text='')
        self.brahma_lb.grid(row = 1, column = 1, padx = (0,20),  sticky = "e" )
        add_to_cart_btn = ctk.CTkButton(frame, text="Adicionar ao Carrinho", command=self.add_to_cart)
        add_to_cart_btn.grid(row=2, column=0, columnspan=2, pady=20) 
        
        self.update_price()

    def update_price(self):
        price_skol = self.prices["Skol"].get(self.skol_size.get())
        self.skol_lb.configure(text=f"R$ {price_skol}")
        price_heineken = self.prices["Heineken"].get(self.heineken_size.get())
        self.heineken_lb.configure(text=f"R$ {price_heineken}")
        price_antartica = self.prices["Antartica"].get(self.antartica_size.get())
        self.antartica_lb.configure(text=f"R$ {price_antartica}")
        price_brahma = self.prices["Brahma"].get(self.brahma_size.get())
        self.brahma_lb.configure(text=f"R$ {price_brahma}")

    def get_username(self):
        if len(sys.argv) > 1:
            self.username = sys.argv[1]
            print("Username:", self.username)

    def add_to_cart(self): 
        valor1 = 0
        valor2 = 0
        valor3 = 0
        valor4 = 0
        value = 0

        db = connect_db()
        cursor = db.cursor()

        query_check_orders = "SELECT 1 FROM orders WHERE username = %s"
        cursor.execute(query_check_orders, (self.username,))
        order_exists = cursor.fetchone() 

        if order_exists:  # Check if a row was returned
                messagebox.showwarning("Aviso", "Você já possui um pedido em andamento. Aguarde a finalização do pedido atual antes de fazer um novo.")
                db.close()
                cursor.close()
                return
        

        if self.entry_skolQuantity.get():
            try:
                quantity = int(self.entry_skolQuantity.get())
                price = float(self.prices["Skol"].get(self.skol_size.get()) or 0)
                valor1 = price * quantity
                value += valor1
                print(f"Skol ({quantity} x {price:.2f}): R$ {valor1:.2f}")
            except ValueError:
                print("Invalid quantity for Skol")


        if self.entry_heinekenQuantity.get():
            try:
                quantity = int(self.entry_heinekenQuantity.get())
                price = float(self.prices["Heineken"].get(self.heineken_size.get()) or 0)
                valor2 = price * quantity
                value += valor2
                print(f"Heineken ({quantity} x {price:.2f}): R$ {valor2:.2f}")
            except ValueError:
                print("Invalid quantity for Heineken")

        if self.entry_antarticaQuantity.get():
            try:
                quantity = int(self.entry_antarticaQuantity.get())
                price = float(self.prices["Antartica"].get(self.antartica_size.get()) or 0)
                valor3 = price * quantity
                value += valor3
                print(f"Antartica ({quantity} x {price:.2f}): R$ {valor3:.2f}")
            except ValueError:
                print("Invalid quantity for Antartica")

        if self.entry_brahmaQuantity.get():
            try:
                quantity = int(self.entry_brahmaQuantity.get())
                price = float(self.prices["Brahma"].get(self.brahma_size.get()) or 0)
                valor4 = price * quantity
                value += valor4
                print(f"Brahma ({quantity} x {price:.2f}): R$ {valor4:.2f}")
            except ValueError:
                print("Invalid quantity for Brahma")
        if value>0:
            self.total_value = value
            print('Total: R$', value)
            
            db = connect_db()
            cursor = db.cursor()

            try:
                if self.entry_skolQuantity.get():
                    self.insert_cart_item(cursor, "Skol", self.skol_size.get(), int(self.entry_skolQuantity.get()), float(self.prices["Skol"].get(self.skol_size.get()) or 0))
                if self.entry_heinekenQuantity.get():
                    self.insert_cart_item(cursor, "Heineken", self.heineken_size.get(), int(self.entry_heinekenQuantity.get()), float(self.prices["Heineken"].get(self.heineken_size.get()) or 0))
                if self.entry_antarticaQuantity.get():
                    self.insert_cart_item(cursor, "Antartica", self.antartica_size.get(), int(self.entry_antarticaQuantity.get()), float(self.prices["Antartica"].get(self.antartica_size.get()) or 0))
                if self.entry_brahmaQuantity.get():
                    self.insert_cart_item(cursor, "Brahma", self.brahma_size.get(), int(self.entry_brahmaQuantity.get()), float(self.prices["Brahma"].get(self.brahma_size.get()) or 0))

                db.commit()
                messagebox.showinfo("Sucesso", "Itens adicionados ao carrinho!")
            except mysql.connector.Error as err:
                print(f"Erro ao adicionar ao carrinho: {err}")
                db.rollback()  # Revert changes if there's an error
                messagebox.showerror("Erro", "Erro ao adicionar ao carrinho.")
            finally:
                cursor.close()
                db.close()


    def insert_cart_item(self, cursor, product_name, size, quantity, price):
        query = "INSERT INTO cart_items (username, product_name, size, quantity, price, total_value) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (self.username, product_name, size, quantity, price, self.total_value)
        cursor.execute(query, values)




    def back(self):
        self.destroy()
        subprocess.run(['python', 'loginPF.py'])

    def Cart(self):
        self.destroy()
        subprocess.run(['python', 'cart.py', self.username])

        


if __name__ == "__main__":
    app = App()
    app.mainloop()
