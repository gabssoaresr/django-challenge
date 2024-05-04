import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from frontend.gui.dashboards.base_dashboard import BaseDashboard


class CustomerDashboard(BaseDashboard):
    def __init__(self, master):
        super().__init__(master)
        
        self.tab_control = ttk.Notebook(self)
        
        self.menu_tab = ttk.Frame(self.tab_control)
        self.orders_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.menu_tab, text='Cardápio')
        self.tab_control.add(self.orders_tab, text='Pedidos')
        
        self.tab_control.pack(expand=1, fill='both')

        self.load_menu_tab()
        self.load_orders_tab()
