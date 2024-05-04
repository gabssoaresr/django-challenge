import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
from .helper import Helper, MasterType


class CustomerTab(tk.Frame):
    def __init__(self, master: MasterType):
        super().__init__(master)
        self.master = master
        self.base_url = "http://127.0.0.1:8000/api/v1/"
        self.page = 1
        self.helper = Helper(self)

    def load_customer_tab(self):
        customer_frame = tk.Frame(self.master.customer_tab)
        customer_frame.pack(fill='both', expand=True)

        self.customer_listbox = tk.Listbox(customer_frame, width=100, height=20)
        self.customer_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(customer_frame, orient='vertical', command=self.customer_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.customer_listbox.config(yscrollcommand=scrollbar.set)

        add_button = tk.Button(self.master.customer_tab, text="Adicionar Cliente", command=self.add_customer)
        add_button.pack(side='left', padx=10)

        update_button = tk.Button(self.master.customer_tab, text="Atualizar Cliente", command=self.update_selected_customer)
        update_button.pack(side='left', padx=10)

        self.reload_button = tk.Button(self.master.customer_tab, text="↻", font=('Arial', 10), command=self.reload_customer_page)
        self.reload_button.pack(side='left', padx=10)

        self.previous_button = tk.Button(self.master.customer_tab, text="<", command=self.load_previous_page)
        self.previous_button.pack(side='left', padx=10)
        self.next_button = tk.Button(self.master.customer_tab, text=">", command=self.load_next_page)
        self.next_button.pack(side='left', padx=10)

        self.load_customer_page()

    def reload_customer_page(self):
        self.load_customer_page()

    def load_customer_page(self):
        response = requests.get(
            f"{self.base_url}customers/?page={self.page}",
            headers=self.master.headers
        )
        if not response.status_code == 200:
            messagebox.showerror("Erro", "Falha ao carregar clientes.")
            return
        
        self.helper.enable_and_disable_next_and_previous_button(response)

        self.customers = response.json()['results']
        self.customer_listbox.delete(0, tk.END)

        header = (
            "Nome".ljust(40) + 
            "E-mail".ljust(40) + 
            "Telefone\n"
        )
        self.customer_listbox.insert(tk.END, header)

        for customer in self.customers:
            name = customer.get('name', '').ljust(40)
            email = customer.get('email', '').ljust(40)
            phone = customer.get('phone', '')

            display_text = f"{name}{email}{phone}\n"
            self.customer_listbox.insert(tk.END, display_text)
        
        if not hasattr(self, 'scrollbar_x'):
            self.scrollbar_x = tk.Scrollbar(self.master.customer_tab, orient=tk.HORIZONTAL)
            self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            self.customer_listbox.config(xscrollcommand=self.scrollbar_x.set)
            self.scrollbar_x.config(command=self.customer_listbox.xview)

    def update_selected_customer(self):
        selected_index = self.customer_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aviso", "Nenhum cliente selecionado. Por favor, selecione um cliente para atualizar.")
            return
        
        selected_customer_index = selected_index[0]
        selected_customer = self.customers[selected_customer_index - 1]

        self.selected_customer = selected_customer

        name = selected_customer['name']
        email = selected_customer['email']
        phone = selected_customer['phone']

        self.update_customer_window = tk.Toplevel(self)
        self.update_customer_window.title("Atualizar Cliente")
        self.update_customer_window.geometry("600x400")

        name_label = tk.Label(self.update_customer_window, text="Nome:")
        name_label.pack()

        self.name_entry = tk.Entry(self.update_customer_window)
        self.name_entry.insert(tk.END, name)  
        self.name_entry.pack()

        email_label = tk.Label(self.update_customer_window, text="E-mail:")
        email_label.pack()

        self.email_entry = tk.Entry(self.update_customer_window)
        self.email_entry.insert(tk.END, email) 
        self.email_entry.pack()

        phone_label = tk.Label(self.update_customer_window, text="Telefone:")
        phone_label.pack()

        self.phone_entry = tk.Entry(self.update_customer_window)
        self.phone_entry.insert(tk.END, phone) 
        self.phone_entry.pack()

        submit_button = tk.Button(self.update_customer_window, text="Atualizar", command=self.submit_updated_customer)
        submit_button.pack()

        back_button = tk.Button(self.update_customer_window, text="Voltar", command=self.update_customer_window.destroy)
        back_button.place(x=10, y=10)

    def submit_updated_customer(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        payload = {
            'name': name,
            'email': email,
            'phone': phone,
        }
        
        response = requests.put(
            f"{self.base_url}customers/{self.selected_customer['id']}/", 
            json=payload,
            headers=self.master.headers,
        )
        if not response.status_code == 200:
            messagebox.showerror("Erro", "Falha ao atualizar cliente. Por favor, tente novamente.")
            return
        
        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        self.load_customer_page()
        self.update_customer_window.destroy() 


    def add_customer(self):
        self.add_customer_window = tk.Toplevel(self)
        self.add_customer_window.title("Adicionar Cliente")
        self.add_customer_window.geometry("600x400")

        name_label = tk.Label(self.add_customer_window, text="Nome:")
        name_label.pack()

        self.name_entry = tk.Entry(self.add_customer_window)
        self.name_entry.pack()

        email_label = tk.Label(self.add_customer_window, text="E-mail:")
        email_label.pack()

        self.email_entry = tk.Entry(self.add_customer_window)
        self.email_entry.pack()

        phone_label = tk.Label(self.add_customer_window, text="Telefone:")
        phone_label.pack()

        self.phone_entry = tk.Entry(self.add_customer_window)
        self.phone_entry.pack()

        submit_button = tk.Button(self.add_customer_window, text="Adicionar", command=self.submit_customer)
        submit_button.pack()

        back_button = tk.Button(self.add_customer_window, text="Voltar", command=self.add_customer_window.destroy)
        back_button.place(x=10, y=10)

    def submit_customer(self):
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        payload = {
            'name': name,
            'email': email,
            'phone': phone,
        }

        response = requests.post(
            f"{self.base_url}customers/", 
            json=payload,
            headers=self.master.headers,
        )
        
        if response.status_code == 201:
            messagebox.showinfo("Sucesso", "Cliente adicionado com sucesso!")
            self.load_customer_page()
            self.add_customer_window.destroy() 
            return
        
        messagebox.showerror("Erro", "Falha ao adicionar cliente. Por favor, tente novamente.")

    def load_next_page(self):
        self.page = self.helper.load_next_page(self.page)
        self.load_customer_page()

    def load_previous_page(self):
        self.page = self.helper.load_previous_page(self.page)
        self.load_customer_page()
