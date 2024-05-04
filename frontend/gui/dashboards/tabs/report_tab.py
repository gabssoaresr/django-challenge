import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import requests
import webbrowser
from .helper import Helper, MasterType


class ReportTab(tk.Frame):
    def __init__(self, master: MasterType):
        super().__init__(master)
        self.master = master
        self.base_url = "http://127.0.0.1:8000/api/v1/"

    def load_report_tab(self):
        report_frame = tk.Frame(self.master.report_tab)
        report_frame.pack(fill='both', expand=True)

        title_label = tk.Label(report_frame, text="Relatório Anual", font=('Arial', 20, 'bold'))
        title_label.pack(pady=20)

        generate_button = tk.Button(report_frame, text="Gerar Relatório", command=self.generate_report)
        generate_button.pack()

    def generate_report(self):
        response = requests.get(
            f"{self.base_url}generate-report/",
            headers=self.master.headers
        )
        if not response.status_code == 200:
            messagebox.showerror("Erro", "Falha ao gerar o relatório.")
            return
        
        download_link = response.json().get('download_url')
        if not download_link:
            messagebox.showerror("Erro", "O link de download do relatório não está disponível.")
            return
        
        messagebox.showinfo("Download", "Clique no link abaixo para baixar o relatório.")
        self.open_download_link(download_link)            
            
    def open_download_link(self, download_link):
        webbrowser.open_new(download_link)
