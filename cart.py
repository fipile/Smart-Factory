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
import re

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
        self.username = self.get_username()
        self.address_data = {}  # To store address data
        self.system()

    def layout_config(self):
        self.title('Smart Factory')
        self.geometry("800x600+100+50")
        self.resizable(width= False, height= False)
    
    def system(self):
        self.home_btn =ctk.CTkButton(self, text="Home", width=100, fg_color='#772581',command= self.home, hover_color='black')
        self.home_btn.place(x=10, y=10)
        self.back_btn = ctk.CTkButton(self, text="Voltar", width=100, fg_color='#772581',command= self.back, hover_color='black')
        self.back_btn.place(x=10, y=560)
        styles.CartFunctions(self)

        self.cart = ctk.CTkLabel(master=self, text="Carrinho", font=('Century Gothic bold', 16), text_color=["#fff", '#fff'])
        self.cart.place(x= 70, y=70)
        self.cart_items_frame = ctk.CTkFrame(master=self, width=600, height=200, corner_radius=10, fg_color='white')
        self.cart_items_frame.place(x=70, y=100)
        self.display_cart_items()

        self.order = ctk.CTkLabel(master=self, text="Seus Pedidos", font=('Century Gothic bold', 16), text_color=["#fff", '#fff'])
        self.order.place(x= 70, y=320)
        self.orders_items_frame = ctk.CTkFrame(master=self, width=600, height=200, corner_radius=10, fg_color='white')
        self.orders_items_frame.place(x=70, y=350)
        self.display_orders_items()

        self.delivery_frame = ctk.CTkFrame(master=self, width=400, height=100, corner_radius=10, fg_color='white')
        self.delivery_frame.place(x=400, y=50)
        self.show_delivery_selection()

    def get_username(self):
        if len(sys.argv) > 1:
            return sys.argv[1]
        else:
            return ""  # Or handle the case where username is not passed
    def display_orders_items(self):
        db = connect_db()
        cursor = db.cursor(dictionary=True)

        try:
            query = "SELECT * FROM orders WHERE username = %s"
            cursor.execute(query, (self.username,))
            order_items = cursor.fetchall()

            # Clear any previous items in the frame
            for widget in self.orders_items_frame.winfo_children():
                widget.destroy()

            if order_items:
                for i, item in enumerate(order_items):
                    # Display item details (adjust formatting as needed)
                    item_label = ctk.CTkLabel(self.orders_items_frame, text=f"{item['product_name']} - {item['size']} x {item['quantity']} - R$ {item['price']:.2f} - Total: R$ {item['total_value']:.2f}")
                    item_label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            else:
                ctk.CTkLabel(self.orders_items_frame, text="Aqui aparecerão seus pedidos.").pack(pady=20)

        except mysql.connector.Error as err:
            print(f"Erro ao buscar itens do carrinho: {err}")
            messagebox.showerror("Erro", "Erro ao carregar o carrinho.")
        finally:
            cursor.close()
            db.close()


    def display_cart_items(self):
        db = connect_db()
        cursor = db.cursor(dictionary=True)  # Use dictionary=True

        try:
            query = "SELECT * FROM cart_items WHERE username = %s"
            cursor.execute(query, (self.username,))
            cart_items = cursor.fetchall()

            # Clear any previous items in the frame
            for widget in self.cart_items_frame.winfo_children():
                widget.destroy()

            if cart_items:
                for i, item in enumerate(cart_items):
                    # Display item details (adjust formatting as needed)
                    item_label = ctk.CTkLabel(self.cart_items_frame, text=f"{item['product_name']} - {item['size']} x {item['quantity']} - R$ {item['price']:.2f} - Total: R$ {item['total_value']:.2f}")
                    item_label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
            else:
                ctk.CTkLabel(self.cart_items_frame, text="Seu carrinho está vazio.").pack(pady=20)

        except mysql.connector.Error as err:
            print(f"Erro ao buscar itens do carrinho: {err}")
            messagebox.showerror("Erro", "Erro ao carregar o carrinho.")
        finally:
            cursor.close()
            db.close()

    def show_delivery_selection(self):
        # Função para exibir os botões de seleção de entrega
        for widget in self.delivery_frame.winfo_children():
            widget.destroy()

        self.delivery_label = ctk.CTkLabel(self.delivery_frame, text="Escolha a forma de entrega:",
                                          font=('Century Gothic bold', 18))
        self.delivery_label.grid(row=0, column=0, pady=20, padx=20, sticky="ew")

        self.pickup_btn = ctk.CTkButton(self.delivery_frame, text="Buscar na Loja", width=200,
                                              fg_color='#772581', hover_color='black',
                                              command=self.process_pickup)
        self.pickup_btn.grid(row=1, column=0, pady=10, padx=20, sticky="ew")

        self.delivery_btn = ctk.CTkButton(self.delivery_frame, text="Entrega", width=200,
                                            fg_color='#772581', hover_color='black',
                                            command=self.show_address_form)
        self.delivery_btn.grid(row=2, column=0, pady=10, padx=20, sticky="ew")

    def show_address_form(self):
        # Função para exibir o formulário de endereço
        for widget in self.delivery_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.delivery_frame, text="Rua:").grid(row=0, column=0, padx=20, pady=10)
        self.street_entry = ctk.CTkEntry(self.delivery_frame)
        self.street_entry.grid(row=0, column=1, padx=20, pady=10)
        self.street_entry.insert(0, self.address_data.get("street", ""))  # Repopulate street

        ctk.CTkLabel(self.delivery_frame, text="Número:").grid(row=1, column=0, padx=20, pady=10)
        self.number_entry = ctk.CTkEntry(self.delivery_frame)
        self.number_entry.grid(row=1, column=1, padx=20, pady=10)
        self.number_entry.insert(0, self.address_data.get("number", ""))  # Repopulate number

        ctk.CTkLabel(self.delivery_frame, text="Bairro:").grid(row=2, column=0, padx=20, pady=10)
        self.neighborhood_entry = ctk.CTkEntry(self.delivery_frame)
        self.neighborhood_entry.grid(row=2, column=1, padx=20, pady=10)
        self.neighborhood_entry.insert(0, self.address_data.get("neighborhood", ""))  # Repopulate neighborhood

        ctk.CTkLabel(self.delivery_frame, text="CEP:").grid(row=3, column=0, padx=20, pady=10)
        self.cep_entry = ctk.CTkEntry(self.delivery_frame)
        self.cep_entry.grid(row=3, column=1, padx=20, pady=10)
        self.cep_entry.insert(0, self.address_data.get("cep", ""))  # Repopulate CEP

        ctk.CTkLabel(self.delivery_frame, text="Cidade:").grid(row=4, column=0, padx=20, pady=10)
        self.city_entry = ctk.CTkEntry(self.delivery_frame)
        self.city_entry.grid(row=4, column=1, padx=20, pady=10)
        self.city_entry.insert(0, self.address_data.get("city", ""))  # Repopulate city

        self.confirm_btn = ctk.CTkButton(self.delivery_frame, text="Confirmar Entrega", command=self.process_delivery)
        self.confirm_btn.grid(row=5, column=0, columnspan=2, pady=20)

        self.back_to_delivery_selection_btn = ctk.CTkButton(self.delivery_frame, text="Voltar",
                                                           command=self.save_and_back_to_delivery_selection)
        self.back_to_delivery_selection_btn.grid(row=6, column=0, columnspan=2, pady=10)

    def validar_cep(self, cep):
        cep = cep.replace('-', '')  # Remove hyphen if present
        cep = re.sub(r'\D', '', cep)  # Remove any remaining non-digit characters
        return cep if len(cep) == 8 else None

    def validar_endereco(self, rua, numero, bairro, cidade):
        """Valida os campos de endereço."""
        if not rua:
            messagebox.showerror("Erro", "O campo 'Rua' é obrigatório.")
            return False
        if not numero:
            messagebox.showerror("Erro", "O campo 'Número' é obrigatório.")
            return False
        if not bairro:
            messagebox.showerror("Erro", "O campo 'Bairro' é obrigatório.")
            return False
        if not cidade:
            messagebox.showerror("Erro", "O campo 'Cidade' é obrigatório.")
            return False
        return True

    def process_delivery(self):
        street = self.street_entry.get()
        number = self.number_entry.get()
        neighborhood = self.neighborhood_entry.get()
        cep = self.cep_entry.get()
        city = self.city_entry.get()

        cleaned_cep = self.validar_cep(cep) 
        if cleaned_cep is None:
            messagebox.showerror("Erro", "CEP inválido!")
            return

        if not self.validar_endereco(street, number, neighborhood, city):
            return

        db = connect_db()
        cursor = db.cursor()

        query_check_orders = "SELECT 1 FROM orders WHERE username = %s"
        cursor.execute(query_check_orders, (self.username,))
        order_exists = cursor.fetchone() 

        if order_exists:  
                messagebox.showwarning("Aviso", "Você já possui um pedido em andamento. Aguarde a finalização do pedido atual antes de fazer um novo.")
                return

        try:
  


            query_cart_count = "SELECT COUNT(*) FROM cart_items WHERE username = %s"
            cursor.execute(query_cart_count, (self.username,))
            cart_count = cursor.fetchone()[0]

            if cart_count == 0:
                messagebox.showwarning("Aviso", "Seu carrinho está vazio!")
                return

            # Insert address into the 'address' table
            query_address = "INSERT INTO address (username, rua, numero, bairro, cep, cidade) VALUES (%s, %s, %s, %s, %s, %s)"
            values_address = (self.username, street, number, neighborhood, cleaned_cep, city)
            cursor.execute(query_address, values_address)

            # Get cart items for the current user
            query_cart = "SELECT * FROM cart_items WHERE username = %s"
            cursor.execute(query_cart, (self.username,))
            cart_items = cursor.fetchall()

            # Insert cart items into the 'orders' table
            for item in cart_items:
                query_orders = "INSERT INTO orders (username, product_name, size, quantity, price, total_value) VALUES (%s, %s, %s, %s, %s, %s)"
                values_orders = (item[1], item[2], item[3], item[4], item[5], item[6])  # Assuming column order in cart_items matches orders
                cursor.execute(query_orders, values_orders)

            # Clear the cart after successful transfer to orders
            self.clear_cart()

            db.commit()
            messagebox.showinfo("Sucesso", "Pedido realizado com sucesso!")

        except mysql.connector.Error as err:
            print(f"Erro ao processar pedido: {err}")
            db.rollback()
            messagebox.showerror("Erro", "Erro ao processar pedido.")
        finally:
            cursor.close()
            db.close()

    def save_and_back_to_delivery_selection(self):
        # Save address data before going back
        self.address_data["street"] = self.street_entry.get()
        self.address_data["number"] = self.number_entry.get()
        self.address_data["neighborhood"] = self.neighborhood_entry.get()
        self.address_data["cep"] = self.cep_entry.get()
        self.address_data["city"] = self.city_entry.get()

        self.show_delivery_selection()

    def process_pickup(self):
        print("Pedido para buscar na loja.")

        db = connect_db()
        cursor = db.cursor()

        try:
            # Check if the cart is empty
            query_cart_count = "SELECT COUNT(*) FROM cart_items WHERE username = %s"
            cursor.execute(query_cart_count, (self.username,))
            cart_count = cursor.fetchone()[0]

            if cart_count == 0:
                messagebox.showwarning("Aviso", "Seu carrinho está vazio!")
                return  # Stop processing if cart is empty

            # Get cart items for the current user
            query_cart = "SELECT * FROM cart_items WHERE username = %s"
            cursor.execute(query_cart, (self.username,))
            cart_items = cursor.fetchall()

            # Insert cart items into the 'orders' table
            for item in cart_items:
                query_orders = "INSERT INTO orders (username, product_name, size, quantity, price, total_value) VALUES (%s, %s, %s, %s, %s, %s)"
                values_orders = (item[1], item[2], item[3], item[4], item[5], item[6])  # Assuming column order in cart_items matches orders
                cursor.execute(query_orders, values_orders)

            # Clear the cart after successful transfer to orders
            self.clear_cart()

            db.commit()
            messagebox.showinfo("Sucesso", "Pedido realizado com sucesso!")
            self.destroy()
            subprocess.run(['python', 'main.py'])

        except mysql.connector.Error as err:
            print(f"Erro ao processar pedido: {err}")
            db.rollback()
            messagebox.showerror("Erro", "Erro ao processar pedido.")
        finally:
            cursor.close()
            db.close()

    def clear_cart(self):
        db = connect_db()
        cursor = db.cursor()
        try:
            query = "DELETE FROM cart_items WHERE username = %s"
            cursor.execute(query, (self.username,))
            db.commit()
            messagebox.showinfo("Sucesso", "Carrinho esvaziado com sucesso!")
            self.display_cart_items()  # Atualiza a exibição do carrinho
        except mysql.connector.Error as err:
            print(f"Erro ao esvaziar o carrinho: {err}")
            messagebox.showerror("Erro", "Erro ao esvaziar o carrinho.")
        finally:
            cursor.close()
            db.close()

    def process_delivery(self):
        street = self.street_entry.get()
        number = self.number_entry.get()
        neighborhood = self.neighborhood_entry.get()
        cep = self.cep_entry.get()
        city = self.city_entry.get()

        if not self.validar_cep(cep):
            messagebox.showerror("Erro", "CEP inválido!")
            return

        if not self.validar_endereco(street, number, neighborhood, city):
            return

        db = connect_db()
        cursor = db.cursor()

        try:
            # Insert address into the 'address' table
            query_address = "INSERT INTO address (username, rua, numero, bairro, cep, cidade) VALUES (%s, %s, %s, %s, %s, %s)"
            values_address = (self.username, street, number, neighborhood, cep, city)
            cursor.execute(query_address, values_address)

            # Get cart items for the current user
            query_cart = "SELECT * FROM cart_items WHERE username = %s"
            cursor.execute(query_cart, (self.username,))
            cart_items = cursor.fetchall()

            # Insert cart items into the 'orders' table
            for item in cart_items:
                query_orders = "INSERT INTO orders (username, product_name, size, quantity, price, total_value) VALUES (%s, %s, %s, %s, %s, %s)"
                values_orders = (item[1], item[2], item[3], item[4], item[5], item[6])  # Assuming column order in cart_items matches orders
                cursor.execute(query_orders, values_orders)

            # Clear the cart after successful transfer to orders
            self.clear_cart()

            db.commit()
            messagebox.showinfo("Sucesso", "Pedido realizado com sucesso!")
            self.destroy()
            subprocess.run(['python', 'main.py'])


        except mysql.connector.Error as err:
            print(f"Erro ao processar pedido: {err}")
            db.rollback()
            messagebox.showerror("Erro", "Erro ao processar pedido.")
        finally:
            cursor.close

    def home(self):
        self.destroy()
        subprocess.run(['python', 'main.py'])

    def back(self):
        self.destroy()
        subprocess.run(['python', 'clientprices.py', self.username])



if __name__ == "__main__":
    app = App()
    app.mainloop()
