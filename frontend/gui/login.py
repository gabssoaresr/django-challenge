import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
from frontend.schemas.login_schema import LoginSchema


class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack()

        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.password_label = tk.Label(self, text="Senha:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = tk.Button(self, text="Login", command=self.login)
        self.login_button.pack()

    def login(self) -> LoginSchema:
        email = self.email_entry.get()
        password = self.password_entry.get()
        payload = {"email": email, "password": password}
        response = requests.post("http://127.0.0.1:8000/api/v1/login/", data=payload)

        if response.status_code == 200:
            login_schema = LoginSchema(**response.json())
            return self.master.show_dashboard(login_schema)

        messagebox.showerror("Erro", "Usuário ou senha incorretos.")