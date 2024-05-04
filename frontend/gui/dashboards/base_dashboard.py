import tkinter as tk
from frontend.gui.dashboards.tabs.menu_item_tab import MenuItemTab
from frontend.gui.dashboards.tabs.customer_tab import CustomerTab
from frontend.gui.dashboards.tabs.order_tab import OrderTab
from frontend.gui.dashboards.tabs.report_tab import ReportTab


class BaseDashboard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        
        self.base_url = "http://127.0.0.1:8000/api/v1/"
        self.page = 1

    def load_reports_tab(self):
        self.master.report_tab = self.report_tab
        ReportTab(self.master).load_report_tab()
     
    def load_customer_tab(self):
        self.master.customer_tab = self.customer_tab
        CustomerTab(self.master).load_customer_tab()

    def load_menu_tab(self):
        self.master.menu_tab = self.menu_tab
        MenuItemTab(self.master).load_menu_tab()

    def load_orders_tab(self):
        self.master.orders_tab = self.orders_tab
        OrderTab(self.master).load_orders_tab()
    