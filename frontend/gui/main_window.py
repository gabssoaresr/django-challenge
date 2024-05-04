import base64
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from frontend.gui.login import LoginFrame
from frontend.gui.dashboards.admin_dashboard import AdminDashboard
from frontend.gui.dashboards.customer_dashboard import CustomerDashboard
from frontend.gui.dashboards.employee_dashboard import EmployeeDashboard
from frontend.schemas.login_schema import LoginSchema


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SF Café - Sistema de Gerenciamento")
        self.geometry("900x900")
        self.user = None
        self.headers = None

        self.login_frame = LoginFrame(self)
        self.login_frame.pack(fill=tk.BOTH, expand=True)

    def show_dashboard(self, login_schema: LoginSchema):
        self.login_frame.destroy()
        self.user = login_schema.user 

        authorization_header = f"Token {login_schema.token}"

        self.headers = {'Authorization': authorization_header}

        if self.user.is_superuser:
            self.admin_dashboard = AdminDashboard(self)
            self.admin_dashboard.pack(fill=tk.BOTH, expand=True)
            return

        elif self.user.is_staff:
            self.employee_dashboard = EmployeeDashboard(self)
            self.employee_dashboard.pack(fill=tk.BOTH, expand=True)
            return

        self.customer_dashboard = CustomerDashboard(self)
        self.customer_dashboard.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
