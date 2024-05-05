import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import requests
from .helper import Helper, MasterType


class OrderTab(tk.Frame):
    PAYMENT_CHOICES = [
        ('pix', 'PIX'),
        ('cash', 'Dinheiro'),
        ('debit', 'Débito'),
        ('credit', 'Crédito'),
    ]
    
    def __init__(self, master: MasterType):
        super().__init__(master)
        self.master = master
        self.base_url = "http://127.0.0.1:8000/api/v1/"
        self.order_page = 1
        self.order_details_page = 1
        self.helper = Helper(self)
        self.selected_order = {}
        
    def load_orders_tab(self):
        order_frame = tk.Frame(self.master.orders_tab)
        order_frame.pack(fill='both', expand=True)
        
        self.order_listbox = tk.Listbox(order_frame, width=100, height=20)
        self.order_listbox.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(order_frame, orient='vertical', command=self.order_listbox.yview)
        scrollbar.pack(side='right', fill='y')
        self.order_listbox.config(yscrollcommand=scrollbar.set)

        add_button = tk.Button(self.master.orders_tab, text="Criar Pedido", command=self.add_order)
        add_button.pack(side='left', padx=10)

        if self.master.user.is_staff:
            finish_order_button = tk.Button(self.master.orders_tab, text="Finalizar Pedido", command=self.finish_order)
            finish_order_button.pack(side='left', padx=10)

        detail_button = tk.Button(self.master.orders_tab, text="Ver Detalhes do Pedido", command=self.load_order_details_page)
        detail_button.pack(side='left', padx=10)

        reload_button = tk.Button(self.master.orders_tab, text="↻", command=self.reload_order_page)
        reload_button.pack(side='right', padx=10)

        self.previous_button = tk.Button(self.master.orders_tab, text="<", command=self.load_order_previous_page)
        self.previous_button.pack(side='left', padx=10)
        self.next_button = tk.Button(self.master.orders_tab, text=">", command=self.load_order_next_page)
        self.next_button.pack(side='left', padx=10)

        self.load_orders_page()

    def reload_order_page(self):
        self.load_orders_page()

    def load_orders_page(self):
        response = requests.get(
            f"{self.base_url}orders/?page={self.order_page}",
            headers=self.master.headers
        )
        if not response.status_code == 200:
            messagebox.showerror("Erro", "Falha ao carregar pedidos.")
            return
        
        self.helper.enable_and_disable_next_and_previous_button(response)

        self.orders = response.json()['results']
        self.order_listbox.delete(0, tk.END)

        header = (
            "ID do Pedido".ljust(20) + 
            "Cliente".ljust(20) + 
            "Total do Pedido".ljust(30) + 
            "Data do Pedido\n"
        )
        self.order_listbox.insert(tk.END, header)

        for order in self.orders:
            order_id = str(order.get('id', '')).ljust(25)
            customer = order['customer']['name'].ljust(25) if order.get('customer') else '' 
            total_order = str(order['total_order']).ljust(30) if order.get('total_order') else ''.ljust(35)
            order_date = str(order.get('order_date', '')).ljust(30)

            display_text = f"{order_id}{customer}{total_order}{order_date}\n"
            self.order_listbox.insert(tk.END, display_text)
        
        if hasattr(self, 'scrollbar_x'):
            return
        
        self.scrollbar_x = tk.Scrollbar(self.master.orders_tab, orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.order_listbox.config(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.config(command=self.order_listbox.xview)

    def add_order(self):
        if not self.master.user.is_staff:
            self.customer_id = self.master.user.id
            return self.submit_order()
        
        self.add_order_window = tk.Toplevel(self)
        self.add_order_window.title("Adicionar Pedido")
        self.add_order_window.geometry("600x400")

        email_label = tk.Label(self.add_order_window, text="Email do Cliente:")
        email_label.pack()

        self.email_entry = tk.Entry(self.add_order_window)
        self.email_entry.pack()

        search_button = tk.Button(self.add_order_window, text="Buscar Cliente", command=self.search_customer)
        search_button.pack()

        submit_button = tk.Button(self.add_order_window, text="Adicionar", command=self.submit_order)
        submit_button.pack()

        back_button = tk.Button(self.add_order_window, text="Voltar", command=self.add_order_window.destroy)
        back_button.place(x=10, y=10)

    def search_customer(self):
        email = self.email_entry.get()
        if not email:
            messagebox.showwarning("Aviso", "Por favor, insira o e-mail do cliente.")
            return 
        
        response = requests.get(
            f"{self.base_url}customers/?email={email}",
            headers=self.master.headers,
        )

        if not response.status_code == 200:
            messagebox.showerror("Erro", "Falha ao buscar cliente. Por favor, tente novamente.")
            return

        customers = response.json()['results']
        if not customers:
            messagebox.showerror("Erro", "Nenhum cliente encontrado com o e-mail fornecido.")
            return
            
        self.customers = customers
        self.customer_search_window = tk.Toplevel(self)
        self.customer_search_window.title("Resultados da Pesquisa de Clientes")

        self.customer_listbox = tk.Listbox(self.customer_search_window, width=50, height=10)
        self.customer_listbox.pack()

        for customer in customers:
            self.customer_listbox.insert(tk.END, f"{customer['name']} - {customer['email']}")

        select_button = tk.Button(self.customer_search_window, text="Selecionar Cliente", command=self.select_customer)
        select_button.pack()

    def select_customer(self):
        selected_index = self.customer_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aviso", "Nenhum cliente selecionado. Por favor, selecione um cliente.")
            return

        selected_customer = self.customers[selected_index[0] - 1]

        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(tk.END, selected_customer['email'])
        self.customer_id = selected_customer['id']
        self.customer_search_window.destroy()
      
    def submit_order(self):
        customer_id = self.customer_id

        payload = {
            'customer': customer_id,
        }

        response = requests.post(
            f"{self.base_url}orders/", 
            json=payload,
            headers=self.master.headers,
        )
        
        if not response.status_code == 201:
            messagebox.showerror("Erro", "Falha ao adicionar pedido. Por favor, tente novamente.")
            return
        
        messagebox.showinfo("Sucesso", "Pedido adicionado com sucesso!")
        self.load_orders_page()

        if hasattr(self, 'add_order_window'):
            self.add_order_window.destroy() 
    
    def finish_order(self):
        self.finalize_order_window = tk.Toplevel(self)
        self.finalize_order_window.title("Finalizar Pedido")
        self.finalize_order_window.geometry("400x200")

        selected_index = self.order_listbox.curselection()

        if not selected_index:
            messagebox.showwarning("Aviso", "Nenhum pedido selecionado. Por favor, selecione um pedido.")
            return

        selected_order_index = selected_index[0] - 1
        self.selected_order = self.orders[selected_order_index]

        self.order_id = self.selected_order.get('id', '')
        total_order = self.selected_order.get('total_order', '')

        total_order_label = tk.Label(self.finalize_order_window, text=f"Valor Total: {total_order}")
        total_order_label.pack()

        payment_label = tk.Label(self.finalize_order_window, text="Selecione o método de pagamento:")
        payment_label.pack()

        self.payment_var = tk.StringVar(self.finalize_order_window)
        self.payment_var.set(self.PAYMENT_CHOICES[0][0])

        payment_options = tk.OptionMenu(self.finalize_order_window, self.payment_var, *self.PAYMENT_CHOICES)
        payment_options.pack()

        finalize_button = tk.Button(self.finalize_order_window, text="Finalizar Pedido", command=self.submit_finish_order)
        finalize_button.pack()

    def submit_finish_order(self):
        selected_payment = self.payment_var.get()

        selected_index = self.order_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aviso", "Nenhum pedido selecionado. Por favor, selecione um pedido.")
            return

        payload = {
            'payment_method': selected_payment,
            'status': 'finished',
        }

        response = requests.put(
            f"{self.base_url}orders/{self.order_id}/",
            json=payload,
            headers=self.master.headers,
        )

        if not response.status_code == 200:
            messagebox.showerror("Erro", "Falha ao finalizar o pedido. Por favor, tente novamente.")
            self.finalize_order_window.destroy()
            return
        
        messagebox.showinfo("Sucesso", "Pedido finalizado com sucesso!")
        self.load_orders_page()
        self.finalize_order_window.destroy()

    def load_order_details_page(self):
        selected_index = self.order_listbox.curselection()
        selected_order_id_exists = self.selected_order.get('id')

        if not selected_index and not selected_order_id_exists:
            messagebox.showwarning("Aviso", "Nenhum pedido selecionado. Por favor, selecione um pedido para ver os detalhes.")
            return

        try:
            selected_order_index = selected_index[0] - 1
            self.selected_order = self.orders[selected_order_index]
        except:
            ...

        self.load_order_details_window()

    def load_order_details_window(self):
        if hasattr(self, 'order_details_window'):
            self.reload_order_details()
            return
        
        self.create_order_details_window()

    def create_order_details_window(self):
        self.order_details_window = tk.Toplevel(self)
        self.order_details_window.title("Detalhes do Pedido")
        self.order_details_window.protocol("WM_DELETE_WINDOW", self.on_order_details_window_close) 

        self.order_details_listbox = tk.Listbox(self.order_details_window, width=100, height=20)
        self.order_details_listbox.pack(fill='both', expand=True)

        self.scrollbar_x = tk.Scrollbar(self.order_details_window, orient=tk.HORIZONTAL)
        self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.order_details_listbox.config(xscrollcommand=self.scrollbar_x.set)
        self.scrollbar_x.config(command=self.order_listbox.xview)

        self.load_order_details()

    def on_order_details_window_close(self):
        if hasattr(self, 'order_details_window'):
            self.next_details_button.destroy()
            self.order_details_window.destroy()
            del self.order_details_window 

    def load_order_details(self):
        if not hasattr(self, 'next_details_button'):  
            self.add_order_details_buttons()

        response = requests.get(
            f"{self.base_url}orders/{self.selected_order['id']}/order-details/?page={self.order_details_page}",
            headers=self.master.headers
        )
        if not response.status_code == 200:
            messagebox.showerror("Erro", "Falha ao carregar detalhes do pedido.")
            return
        
        response_data = response.json()
        next_page = response_data.get('next')
        previous_page = response_data.get('previous')

        self.next_details_button.config(state='normal' if next_page else 'disabled')
        self.previous_details_button.config(state='normal' if previous_page else 'disabled')

        self.update_order_details_listbox(response_data['results'])

    def update_order_details_listbox(self, order_details):
        self.order_details = order_details
        self.order_details_listbox.delete(0, tk.END)
        header = (
            "ID do Pedido".ljust(15) +
            "ID do Item".ljust(15) +
            "Nome do Item".ljust(15) +
            "Quantidade".ljust(15) +
            "Customizações\n"
        )
        self.order_details_listbox.insert(tk.END, header)

        for detail in order_details:
            order_id = str(detail['order']['id']).ljust(22) if detail.get('order') else ''
            detail_id = str(detail.get('id', '')).ljust(22)
            menu_item_name = detail['menu_item']['name'].ljust(22) if detail.get('menu_item') else ''
            quantity = str(detail.get('quantity', '')).ljust(22)
            customizations = detail.get('customizations', '').ljust(30)

            display_text = f"{order_id}{detail_id}{menu_item_name}{quantity}{customizations}\n"
            self.order_details_listbox.insert(tk.END, display_text)

    def add_order_details_buttons(self):
        create_button = tk.Button(self.order_details_window, text="Criar Detalhe do Pedido", command=self.add_order_detail)
        create_button.pack(side='left', padx=10)

        update_button = tk.Button(self.order_details_window, text="Atualizar Detalhe do Pedido", command=self.update_order_detail)
        update_button.pack(side='left', padx=10)
        
        reload_button = tk.Button(self.order_details_window, text="↻", command=self.reload_order_details)
        reload_button.pack(side='right', padx=10)

        self.previous_details_button = tk.Button(self.order_details_window, text="<", command=self.load_order_details_previous_page)
        self.previous_details_button.pack(side='left', padx=10)
        self.next_details_button = tk.Button(self.order_details_window, text=">", command=self.load_order_details_next_page)
        self.next_details_button.pack(side='left', padx=10)

        if not hasattr(self, 'scrollbar_x'):
            self.scrollbar_x = tk.Scrollbar(self.order_details_window, orient=tk.HORIZONTAL)
            self.scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
            self.order_details_listbox.config(xscrollcommand=self.scrollbar_x.set)
            self.scrollbar_x.config(command=self.order_listbox.xview)

    def update_order_detail(self):
        selected_index = self.order_details_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aviso", "Nenhum detalhe do pedido selecionado. Por favor, selecione um detalhe do pedido.")
            return

        selected_index = selected_index[0] - 1
        selected_order_detail = self.order_details[selected_index]

        self.order_detail_id = selected_order_detail['id']
        order_id = selected_order_detail['order']['id']
        self.menu_item_id = selected_order_detail['menu_item']['id']
        quantity = selected_order_detail['quantity']
        customizations = selected_order_detail['customizations']

        self.update_order_detail_window = tk.Toplevel(self)
        self.update_order_detail_window.title("Atualizar Detalhe do Pedido")
        self.update_order_detail_window.geometry("600x400")

        quantity_label = tk.Label(self.update_order_detail_window, text="Quantidade:")
        quantity_label.pack()

        self.quantity_entry = tk.Entry(self.update_order_detail_window)
        self.quantity_entry.insert(tk.END, quantity)
        self.quantity_entry.pack()

        customizations_label = tk.Label(self.update_order_detail_window, text="Customizações:")
        customizations_label.pack()

        self.customizations_entry = tk.Entry(self.update_order_detail_window)
        self.customizations_entry.insert(tk.END, customizations)
        self.customizations_entry.pack()

        submit_button = tk.Button(self.update_order_detail_window, text="Atualizar Detalhe do Pedido", command=self.submit_updated_order_detail)
        submit_button.pack()

        back_button = tk.Button(self.update_order_detail_window, text="Voltar", command=self.update_order_detail_window.destroy)
        back_button.place(x=10, y=10)

    def submit_updated_order_detail(self,):
        quantity = self.quantity_entry.get()
        customizations = self.customizations_entry.get()

        payload = {
            'menu_item_id': self.menu_item_id,
            'quantity': quantity,
            'customizations': customizations,
        }
        
        response = requests.put(
            f"{self.base_url}order-details/{self.order_detail_id}/", 
            json=payload,
            headers=self.master.headers,
        )
        if not response.status_code == 200:
            messagebox.showerror("Erro", "Falha ao atualizar detalhe do pedido. Verifique a disponibilidade do produto")
            return
        
        messagebox.showinfo("Sucesso", "Detalhe do pedido atualizado com sucesso!")
        self.load_order_details_page()
        self.update_order_detail_window.destroy() 


    def reload_order_details(self):
        self.load_order_details()

    def reload_order_details_page(self):
        self.load_order_details_page()

    def add_order_detail(self):
        self.add_order_detail_window = tk.Toplevel(self)
        self.add_order_detail_window.title("Adicionar Detalhe do Pedido")
        self.add_order_detail_window.geometry("600x400")

        menu_item_label = tk.Label(self.add_order_detail_window, text="Item do Menu:")
        menu_item_label.pack()

        self.menu_item_entry = tk.Entry(self.add_order_detail_window)
        self.menu_item_entry.pack()

        search_menu_button = tk.Button(self.add_order_detail_window, text="Buscar Item do Menu", command=self.search_menu_items)
        search_menu_button.pack()

        quantity_label = tk.Label(self.add_order_detail_window, text="Quantidade:")
        quantity_label.pack()

        self.quantity_entry = tk.Entry(self.add_order_detail_window)
        self.quantity_entry.pack()

        customizations_label = tk.Label(self.add_order_detail_window, text="Customizações:")
        customizations_label.pack()

        self.customizations_entry = tk.Entry(self.add_order_detail_window)
        self.customizations_entry.pack()

        submit_button = tk.Button(self.add_order_detail_window, text="Adicionar Detalhe do Pedido", command=self.submit_order_detail)
        submit_button.pack()

        back_button = tk.Button(self.add_order_detail_window, text="Voltar", command=self.add_order_detail_window.destroy)
        back_button.place(x=10, y=10)

    def search_menu_items(self):
        item_name = self.menu_item_entry.get()
        if not item_name:
            messagebox.showwarning("Aviso", "Por favor, insira o nome do item do menu.")
            return 

        response = requests.get(
            f"{self.base_url}menu-items/?name={item_name}", 
            headers=self.master.headers,
        )

        if not response.status_code == 200:
            messagebox.showerror("Erro", "Falha ao buscar itens do menu. Por favor, tente novamente.")
            return

        menu_items = response.json()['results']
        if not menu_items:
            messagebox.showerror("Erro", "Nenhum item do menu encontrado com o nome fornecido.")
            return
            
        self.menu_items = menu_items
        self.menu_item_search_window = tk.Toplevel(self)
        self.menu_item_search_window.title("Resultados da Pesquisa de Itens do Menu")

        self.menu_item_listbox = tk.Listbox(self.menu_item_search_window, width=50, height=10)
        self.menu_item_listbox.pack()

        for menu_item in menu_items:
            self.menu_item_listbox.insert(tk.END, f"{menu_item['name']} - Preço: {menu_item['price']}")

        select_button = tk.Button(self.menu_item_search_window, text="Selecionar Item do Menu", command=self.select_menu_item)
        select_button.pack()

    def select_menu_item(self):
        selected_index = self.menu_item_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Aviso", "Nenhum item do menu selecionado. Por favor, selecione um item do menu.")
            return

        selected_index = selected_index[0] - 1
        selected_menu_item = self.menu_items[selected_index]

        self.menu_item_entry.delete(0, tk.END)
        self.menu_item_entry.insert(tk.END, selected_menu_item['name'])
        self.menu_item_id = selected_menu_item['id']
        self.menu_item_search_window.destroy()

    def submit_order_detail(self):
        order_id = self.selected_order['id']
        menu_item_id = self.menu_item_id
        quantity = self.quantity_entry.get()
        customizations = self.customizations_entry.get()

        payload = {
            'order_id': order_id,
            'menu_item_id': menu_item_id,
            'quantity': quantity,
            'customizations': customizations,
        }
        
        response = requests.post(
            f"{self.base_url}order-details/", 
            json=payload,
            headers=self.master.headers,
        )
        if not response.status_code == 201:
            messagebox.showerror("Erro", "Falha ao adicionar detalhe do pedido. Verifique a disponibilidade do produto.")
            return
        
        messagebox.showinfo("Sucesso", "Detalhe do pedido adicionado com sucesso!")
        self.load_order_details_page()
        self.add_order_detail_window.destroy() 

    def load_order_next_page(self):
        self.order_page = self.helper.load_next_page(self.order_page)
        self.load_orders_page()

    def load_order_previous_page(self):
        self.order_page = self.helper.load_previous_page(self.order_page)
        self.load_orders_page()

    def load_order_details_next_page(self):
        self.order_details_page = self.helper.load_next_page(self.order_details_page)
        self.load_order_details_page()

    def load_order_details_previous_page(self):
        self.order_details_page = self.helper.load_previous_page(self.order_details_page)
        self.load_order_details_page()