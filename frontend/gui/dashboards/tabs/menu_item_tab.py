import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
from .helper import Helper, MasterType


class MenuItemTab(tk.Frame):
    def __init__(self, master: MasterType):
        super().__init__(master)
        self.master = master
        self.base_url = "http://127.0.0.1:8000/api/v1/"
        self.page = 1
        self.helper = Helper(self)

    def load_menu_tab(self):
        menu_frame = tk.Frame(self.master.menu_tab)
        menu_frame.pack(fill='both', expand=True)

        self.menu_items_listbox = tk.Listbox(menu_frame, width=100, height=20)
        self.menu_items_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(menu_frame, orient='vertical', command=self.menu_items_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.menu_items_listbox.config(yscrollcommand=scrollbar.set)

        if self.master.user.is_staff:
            add_button = tk.Button(self.master.menu_tab, text="Adicionar Item", command=self.add_menu_item)
            add_button.pack(side='left', padx=10)

            update_button = tk.Button(self.master.menu_tab, text="Atualizar Item", command=self.update_selected_item)
            update_button.pack(side='left', padx=10)

        reload_button = tk.Button(self.master.menu_tab, text="↻", command=self.reload_customer_page)
        reload_button.pack(side='right', padx=10)

        self.previous_button = tk.Button(self.master.menu_tab, text="<", command=self.load_previous_page)
        self.previous_button.pack(side='left', padx=10)
        self.next_button = tk.Button(self.master.menu_tab, text=">", command=self.load_next_page)
        self.next_button.pack(side='left', padx=10)

        self.load_menu_page()

    def reload_customer_page(self):
        self.load_menu_page()

    def load_menu_page(self):
        response = requests.get(
            f"{self.base_url}menu-items/?page={self.page}&page_size=10", 
            headers=self.master.headers
        )
        if not response.status_code == 200:
            messagebox.showerror("Erro", "Falha ao carregar itens do cardápio.")
            return
        
        self.helper.enable_and_disable_next_and_previous_button(response)

        self.menu_items = response.json()['results']
        self.menu_items_listbox.delete(0, tk.END)

        header = (
            "Nome".ljust(30) + 
            "Preço".ljust(25) + 
            "Descrição".ljust(30) + 
            "Ingredientes".ljust(30) + 
            "Informações Nutricionais".ljust(30) + 
            "Estoque\n")
        self.menu_items_listbox.insert(tk.END, header)

        for item in self.menu_items:
            name = item.get('name', '').ljust(30)
            price = str(item.get('price', '')).ljust(25)
            description = item.get('description', '').ljust(35)
            ingredients = item.get('ingredients', '').ljust(35)
            nutritional_info = item.get('nutritional_information', '').ljust(50)
            inventory = (
                item['inventory']['available_quantity'] 
                if item.get('inventory') 
                else ''
            )

            display_text = f"{name}{price}{description}{ingredients}{nutritional_info}{inventory}\n"
            self.menu_items_listbox.insert(tk.END, display_text)

        if not hasattr(self, 'scrollbar_x'):
            self.scrollbar_x = tk.Scrollbar(self.master.menu_tab, orient=tk.HORIZONTAL)
            self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            self.menu_items_listbox.config(xscrollcommand=self.scrollbar_x.set)
            self.scrollbar_x.config(command=self.menu_items_listbox.xview)

    def update_selected_item(self):
        selected_index = self.menu_items_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aviso", "Nenhum item selecionado. Por favor, selecione um item para atualizar.")
            return
        
        selected_item_index = selected_index[0]
        selected_item = self.menu_items_listbox.get(selected_item_index)

        item = self.menu_items[selected_item_index - 1]
        self.selected_item = item

        name = item['name']
        price = float(item['price'])
        description = item['description']
        ingredients = item['ingredients']
        nutritional_info = item['nutritional_information']
        photo_path = item['photo_path']
        available_quantity = (
            item['inventory']['available_quantity'] 
            if item.get('inventory') 
            else ''
        )

        self.update_item_window = tk.Toplevel(self)
        self.update_item_window.title("Atualizar Item do Cardápio")
        self.update_item_window.geometry("800x700")

        name_label = tk.Label(self.update_item_window, text="Nome:")
        name_label.pack()

        self.name_entry = tk.Entry(self.update_item_window)
        self.name_entry.insert(tk.END, name)  
        self.name_entry.pack()

        price_label = tk.Label(self.update_item_window, text="Preço:")
        price_label.pack()

        self.price_entry = tk.Entry(self.update_item_window, validate="key", validatecommand=(self.register(self.validate_number), "%P"))
        self.price_entry.insert(tk.END, price)
        self.price_entry.pack()

        photo_label = tk.Label(self.update_item_window, text="Foto:")
        photo_label.pack()

        self.photo_path = tk.StringVar()
        self.photo_path.set(photo_path) 
        self.photo_entry = tk.Entry(self.update_item_window, textvariable=self.photo_path)
        self.photo_entry.pack()

        photo_button = tk.Button(self.update_item_window, text="Selecionar Foto", command=self.select_photo)
        photo_button.pack()

        description_label = tk.Label(self.update_item_window, text="Descrição:")
        description_label.pack()

        self.description_entry = tk.Text(self.update_item_window, height=4, width=40)
        self.description_entry.insert(tk.END, description)  
        self.description_entry.pack()

        ingredients_label = tk.Label(self.update_item_window, text="Ingredientes:")
        ingredients_label.pack()

        self.ingredients_entry = tk.Text(self.update_item_window, height=4, width=40)
        self.ingredients_entry.insert(tk.END, ingredients)  
        self.ingredients_entry.pack()

        nutritional_info_label = tk.Label(self.update_item_window, text="Informações Nutricionais:")
        nutritional_info_label.pack()

        self.nutritional_info_entry = tk.Text(self.update_item_window, height=4, width=40)
        self.nutritional_info_entry.insert(tk.END, nutritional_info)  
        self.nutritional_info_entry.pack()

        available_quantity_label = tk.Label(self.update_item_window, text="Quantidade Disponível:")
        available_quantity_label.pack()

        self.available_quantity_entry = tk.Entry(self.update_item_window)
        self.available_quantity_entry.insert(tk.END, available_quantity)  
        self.available_quantity_entry.pack()

        submit_button = tk.Button(self.update_item_window, text="Atualizar", command=self.submit_updated_menu_item)
        submit_button.pack()

        back_button = tk.Button(self.update_item_window, text="Voltar", command=self.update_item_window.destroy)
        back_button.place(x=10, y=10)

    def submit_updated_menu_item(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        photo_path = self.photo_path.get()
        description = self.description_entry.get("1.0", "end-1c")  
        ingredients = self.ingredients_entry.get("1.0", "end-1c")  
        nutritional_info = self.nutritional_info_entry.get("1.0", "end-1c")  

        with open(photo_path, 'rb') as photo_file:
            payload = {
                'name': name,
                'price': price,
                'description': description,
                'ingredients': ingredients,
                'nutritional_information': nutritional_info,
            }

            response = requests.put(
                f"{self.base_url}menu-items/{self.selected_item['id']}/", 
                data=payload, 
                files={'new_photo': photo_file}, 
                headers=self.master.headers,
            )

            if not response.status_code == 200:
                messagebox.showerror("Erro", "Falha ao atualizar item ao cardápio. Por favor, tente novamente.")
                return
            
            messagebox.showinfo("Sucesso", "Item atualizado com sucesso!")
            self.submit_upsert_inventory()
            self.load_menu_page()
            self.update_item_window.destroy()            

    def submit_upsert_inventory(self):
        available_quantity = self.available_quantity_entry.get()

        payload = {
            'available_quantity': available_quantity
        }

        response = requests.post(
            f"{self.base_url}menu-items/{self.selected_item['id']}/inventory/", 
            json=payload, 
            headers=self.master.headers,
        )

        if not response.status_code == 201:
            messagebox.showerror("Erro", "Falha ao atualizar item estoque.")
            return          

    def add_menu_item(self):
        self.add_menu_item_window = tk.Toplevel(self)
        self.add_menu_item_window.title("Adicionar Item ao Cardápio")
        self.add_menu_item_window.geometry("800x700")
    
        name_label = tk.Label(self.add_menu_item_window, text="Nome:")
        name_label.pack()

        self.name_entry = tk.Entry(self.add_menu_item_window)
        self.name_entry.pack()

        price_label = tk.Label(self.add_menu_item_window, text="Preço:")
        price_label.pack()

        self.price_entry = tk.Entry(self.add_menu_item_window, validate="key", validatecommand=(self.register(self.validate_number), "%P"))
        self.price_entry.pack()
        self.price_entry.insert(tk.END, "R$ ")

        photo_label = tk.Label(self.add_menu_item_window, text="Foto:")
        photo_label.pack()
        self.photo_path = tk.StringVar()
        self.photo_entry = tk.Entry(self.add_menu_item_window, textvariable=self.photo_path)
        self.photo_entry.pack()

        photo_button = tk.Button(self.add_menu_item_window, text="Selecionar Foto", command=self.select_photo)
        photo_button.pack()

        description_label = tk.Label(self.add_menu_item_window, text="Descrição:")
        description_label.pack()
        self.description_entry = tk.Text(self.add_menu_item_window, height=4, width=40)
        self.description_entry.pack()

        ingredients_label = tk.Label(self.add_menu_item_window, text="Ingredientes:")
        ingredients_label.pack()
        self.ingredients_entry = tk.Text(self.add_menu_item_window, height=4, width=40)
        self.ingredients_entry.pack()

        nutritional_info_label = tk.Label(self.add_menu_item_window, text="Informações Nutricionais:")
        nutritional_info_label.pack()
        self.nutritional_info_entry = tk.Text(self.add_menu_item_window, height=4, width=40)
        self.nutritional_info_entry.pack()

        available_quantity_label = tk.Label(self.add_menu_item_window, text="Quantidade Disponível:")
        available_quantity_label.pack()
        self.available_quantity_entry = tk.Entry(self.add_menu_item_window)
        self.available_quantity_entry.pack()

        submit_button = tk.Button(self.add_menu_item_window, text="Criar", command=self.submit_menu_item)
        submit_button.pack()

        back_button = tk.Button(self.add_menu_item_window, text="Voltar", command=self.add_menu_item_window.destroy)
        back_button.place(x=10, y=10)

    def select_photo(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.photo_path.set(filename)

    def validate_number(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def submit_menu_item(self):
        name = self.name_entry.get()
        price = self.price_entry.get()
        photo_path = self.photo_path.get()
        description = self.description_entry.get("1.0", "end-1c")  
        ingredients = self.ingredients_entry.get("1.0", "end-1c")  
        nutritional_info = self.nutritional_info_entry.get("1.0", "end-1c")  
        available_quantity = self.available_quantity_entry.get()

        with open(photo_path, 'rb') as photo_file:
            payload = {
                'name': name,
                'price': price,
                'description': description,
                'ingredients': ingredients,
                'nutritional_information': nutritional_info,
            }

            response = requests.post(
                f"{self.base_url}menu-items/", 
                data=payload, 
                files={'new_photo': photo_file}, 
                headers=self.master.headers,
            )

            if not response.status_code == 201:
                messagebox.showerror("Erro", "Falha ao adicionar item ao cardápio. Por favor, tente novamente.")
                return
            
            messagebox.showinfo("Sucesso", "Item adicionado ao cardápio com sucesso!")

            self.selected_item = response.json()
            self.submit_upsert_inventory()
            self.load_menu_page()
            self.add_menu_item_window.destroy() 
            
            
    def load_next_page(self):
        self.page = self.helper.load_next_page(self.page)
        self.load_menu_page()

    def load_previous_page(self):
        self.page = self.helper.load_previous_page(self.page)
        self.load_menu_page()