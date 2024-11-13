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
from sender import send_email
import emailtext


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
        self.user_buttons = []
        self.system()

    def layout_config(self):
        self.title('Smart Factory')
        self.geometry("800x600+100+50")
        self.resizable(width=False, height=False)

    def system(self):
        self.back_btn = ctk.CTkButton(self, text="Voltar", width=100, fg_color='#772581', command=self.back,
                                     hover_color='black')
        self.back_btn.place(x=10, y=560)
        self.home_btn = ctk.CTkButton(self, text="Home", width=100, fg_color='#772581', command=self.home,
                                     hover_color='black')
        self.home_btn.place(x=10, y=10)

        self.orders_frame = ctk.CTkFrame(master=self, width=100, height=450, corner_radius=10, fg_color='white')
        self.orders_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Create a canvas
        self.canvas = tk.Canvas(self.orders_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the canvas
        scrollbar = tk.Scrollbar(self.orders_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create a frame inside the canvas which will be scrolled
        self.buttons_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.buttons_frame, anchor="nw")

        self.display_user_buttons()

    def display_user_buttons(self):
        # Limpa os botões existentes
        for button in self.user_buttons:
            button.destroy()
        self.user_buttons = []

        # Busca os nomes de usuário do banco de dados
        db = connect_db()
        cursor = db.cursor()
        try:
            query = "SELECT username FROM allusers"
            cursor.execute(query)
            usernames = cursor.fetchall()

            # Cria um botão para cada nome de usuário
            for i, username in enumerate(usernames):
                username = username[0]  # Extrai a string da tupla
                button = ctk.CTkButton(self.buttons_frame, text=username,  # Adiciona os botões ao buttons_frame
                                        command=lambda u=username: self.open_user_orders(u))
                button.grid(row=i, column=0, pady=10, padx=10, sticky="ew")
                self.user_buttons.append(button)

        except mysql.connector.Error as err:
            messagebox.showerror("Erro", f"Erro ao buscar nomes de usuário: {err}")
        finally:
            cursor.close()
            db.close()

    def open_user_orders(self, username):
        self.order_window = ctk.CTkToplevel(self)
        self.order_window.transient(self)
        self.order_window.title(f"Pedidos de {username}")
        self.order_window.geometry("600x400+200+200")


        self.order_items_frame = ctk.CTkFrame(self.order_window, width=400, height=300, corner_radius=10,
                                             fg_color='white')
        self.order_items_frame.place(x=20, y=20)

        self.address_frame = ctk.CTkFrame(self.order_window, width=400, height=300, corner_radius=10,
                                          fg_color='white')
        self.address_frame.place(x=370, y=20)

        self.display_order_items(username)
        self.display_user_address(username)

        self.order_status_entry = ctk.CTkEntry(self.order_window, width=200, placeholder_text="Status do Pedido")
        self.order_status_entry.place(x=220, y=320)

        delete_button = ctk.CTkButton(self.order_window, text="Excluir Conta", command=lambda u=username: self.delete_user(u))
        delete_button.place(x=20, y=350)

        cancel_button = ctk.CTkButton(self.order_window, text="Cancelar Compra",
                                     command=lambda u=username: self.cancel_order(u))
        cancel_button.place(x=170, y=350)

        complete_button = ctk.CTkButton(self.order_window, text="Concluir Pedido",
                                       command=lambda u=username: self.complete_order(u))
        complete_button.place(x=320, y=350)

        status_button = ctk.CTkButton(self.order_window, text="Status do Pedido",
                                      command=lambda u=username: self.send_order_status(u))
        status_button.place(x=470, y=350)

    def delete_user(self, username):
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir a conta de {username}?"):
            db = connect_db()
            cursor = db.cursor()
            try:
                
                query_delete_user = "DELETE FROM users WHERE usernames = %s"
                cursor.execute(query_delete_user, (username,))
                query_delete_userpj = "DELETE FROM userpj WHERE username = %s"
                cursor.execute(query_delete_userpj, (username,))
                query_delete_address = "DELETE FROM address WHERE username = %s"
                cursor.execute(query_delete_address, (username,))
                query_delete_orders = "DELETE FROM orders WHERE username = %s"
                cursor.execute(query_delete_orders, (username,))
                query_delete_cart_items = "DELETE FROM cart_items WHERE username = %s"
                cursor.execute(query_delete_cart_items, (username,))
                query_delete_allusers = "DELETE FROM allusers WHERE username = %s"
                cursor.execute(query_delete_allusers, (username,))

                db.commit()


                messagebox.showinfo("Sucesso", f"Conta de {username} excluída com sucesso!")
                self.order_window.destroy() 
                self.display_user_buttons() 
            except mysql.connector.Error as err:
                db.rollback()
                messagebox.showerror("Erro", f"Erro ao excluir usuário: {err}")
            finally:
                cursor.close()
                db.close()
    
    def display_order_items(self, username):
        db = connect_db()
        cursor = db.cursor(dictionary=True)

        try:
            query = "SELECT * FROM orders WHERE username = %s"
            cursor.execute(query, (username,))
            order_items = cursor.fetchall()

            for widget in self.order_items_frame.winfo_children():
                widget.destroy()

            if order_items:
                for i, item in enumerate(order_items):
                    item_label = ctk.CTkLabel(self.order_items_frame,
                                              text=f"{item['product_name']} - {item['size']} x {item['quantity']} - R$ {item['price']:.2f} - Total: R$ {item['total_value']:.2f}")
                    item_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            else:
                ctk.CTkLabel(self.order_items_frame, text="Nenhum pedido encontrado.").pack(pady=20)

        except mysql.connector.Error as err:
            print(f"Erro ao buscar pedidos: {err}")
            messagebox.showerror("Erro", "Erro ao carregar os pedidos.")
        finally:
            cursor.close()
            db.close()

    def display_user_address(self, username):
        db = connect_db()
        cursor = db.cursor(dictionary=True)

        try:
            query = "SELECT * FROM address WHERE username = %s"
            cursor.execute(query, (username,))
            address = cursor.fetchone()

            # Clear any previous address in the frame
            for widget in self.address_frame.winfo_children():
                widget.destroy()

            if address:
                address_label = ctk.CTkLabel(self.address_frame,
                                              text=f"Endereço:\nRua: {address['rua']}, {address['numero']}\nBairro: {address['bairro']}\nCEP: {address['cep']}\nCidade: {address['cidade']}")
                address_label.pack(pady=20)
            else:
                ctk.CTkLabel(self.address_frame, text="Buscar na Loja").pack(pady=20)

        except mysql.connector.Error as err:
            print(f"Erro ao buscar endereço: {err}")
            messagebox.showerror("Erro", "Erro ao carregar o endereço.")
        finally:
            cursor._connection.handle_unread_result()
            cursor.close()
            db.close()

    def cancel_order(self, username):
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja cancelar a compra de {username}?"):
            db = connect_db()
            cursor = db.cursor()
            try:
                # Exclui os pedidos do usuário da tabela 'orders'
                query_delete_orders = "DELETE FROM orders WHERE username = %s"
                cursor.execute(query_delete_orders, (username,))

                query_delete_address = "DELETE FROM address WHERE username = %s"
                cursor.execute(query_delete_address, (username,))
                
                db.commit()
                user_email = self.get_user_email(username)
                if user_email:
                    message = emailtext.cancel_order(user_email)
                    send_email(
                        sender_email="smartfactoryltda@gmail.com",  # Replace with your email
                        sender_password="ygtp tguv ztrh qoed",      # Replace with your password
                        recipient_email=user_email,
                        subject="Cancelamento de Compra",
                        message=message
                    )
                messagebox.showinfo("Sucesso", f"Compra de {username} cancelada com sucesso!")
                self.order_window.destroy()  # Fecha a janela de pedidos
                self.display_order_items(username)  # Atualiza a lista de pedidos
            except mysql.connector.Error as err:
                db.rollback()
                messagebox.showerror("Erro", f"Erro ao cancelar a compra: {err}")
            finally:
                cursor.close()
                db.close()

    def complete_order(self, username):
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja concluir o pedido de {username}?"):
            db = connect_db()
            cursor = db.cursor()
            try:
                # Get user's email
                user_email = self.get_user_email(username)
                if user_email:
                    # Send order completion email
                    message = emailtext.order_done(user_email)
                    send_email(
                        sender_email="smartfactoryltda@gmail.com",  # Replace with your email
                        sender_password="ygtp tguv ztrh qoed",      # Replace with your password
                        recipient_email=user_email,
                        subject="Pedido Concluído",
                        message=message
                    )

                    # Exclui os pedidos do usuário da tabela 'orders' (opcional)
                    query_delete_orders = "DELETE FROM orders WHERE username = %s"
                    cursor.execute(query_delete_orders, (username,))
                    db.commit()

                    messagebox.showinfo("Sucesso", f"Pedido de {username} concluído com sucesso!")
                    self.order_window.destroy()  # Fecha a janela de pedidos
                    self.display_order_items(username)  # Atualiza a lista de pedidos (se necessário)
                else:
                    messagebox.showwarning("Email não encontrado", "O email do usuário não foi encontrado no banco de dados.")
            except mysql.connector.Error as err:
                db.rollback()
                messagebox.showerror("Erro", f"Erro ao concluir o pedido: {err}")
            finally:
                cursor.close()
                db.close()

    def send_order_status(self, username):
        status = self.order_status_entry.get()  # Get the status from the entry
        if not status:
            messagebox.showwarning("Aviso", "Por favor, insira o status do pedido.")
            return

        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja enviar o status '{status}' para {username}?"):
            db = connect_db()
            cursor = db.cursor()
            try:
                # Get user's email
                user_email = self.get_user_email(username)
                if user_email:
                    # Send order status email
                    message = emailtext.order_status(user_email, status) 
                    send_email(
                        sender_email="smartfactoryltda@gmail.com",  # Replace with your email
                        sender_password="ygtp tguv ztrh qoed",      # Replace with your password
                        recipient_email=user_email,
                        subject="Atualização do Status do Pedido",
                        message=message
                    )

                    messagebox.showinfo("Sucesso", f"Status do pedido enviado para {username} com sucesso!")
                else:
                    messagebox.showwarning("Email não encontrado", "O email do usuário não foi encontrado no banco de dados.")
            except mysql.connector.Error as err:
                messagebox.showerror("Erro", f"Erro ao enviar o status do pedido: {err}")
            finally:
                cursor.close()
                db.close()

    def get_user_email(self, username):
        db = connect_db()
        cursor = db.cursor(prepared=True)
        query = "SELECT email FROM users WHERE usernames = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if not result:  # If not found in 'users', try 'userpj'
            query = "SELECT email FROM userpj WHERE username = %s"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
        cursor.close()
        db.close()
        return result[0] if result else None
    

    def back(self):
        self.destroy()
        subprocess.run(['python', 'admin.py'])

    def home(self):
        self.destroy()
        subprocess.run(['python', 'adminlogin.py'])


if __name__ == "__main__":
    app = App()
    app.mainloop()
