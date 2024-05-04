from tkinter import Tk
from typing import TypeVar
from requests.models import Response


MasterType = TypeVar('MasterType', bound=Tk)


class Helper:
    def __init__(self, master: MasterType) -> None:
        self.master = master 

    def load_next_page(self, page: int):
        page += 1
        return page

    def load_previous_page(self, page: int):
        if page > 1:
            page -= 1
        return page
    
    def enable_and_disable_next_and_previous_button(self, response: Response):
        response_data = response.json()
        next_page = response_data.get('next')
        previous_page = response_data.get('previous')

        self.master.next_button.config(state='normal' if next_page else 'disabled')
        self.master.previous_button.config(state='normal' if previous_page else 'disabled')
