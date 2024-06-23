from tkinter import *
from typing import *
from GUI.MapComponentCard import *


class MapComponentsMenu(Frame):
    __card_list: List[MapComponentCard] = []
    __last_amount_of_columns: int = 0
    __last_amount_of_cards: int = 0

    def __init__(self, master: Optional[Misc], **kwargs):
        super().__init__(master, kwargs)

    def add_card(self, card: MapComponentCard):
        self.__last_amount_of_cards = len(self.__card_list)
        self.__card_list.append(card)
        self.update_content()

    def update_content(self):
        columns_amount = self.winfo_width() // 100
        if columns_amount == 0:
            self.after(100,self.update_content)
            return
        if len(self.__card_list) == self.__last_amount_of_cards and self.__last_amount_of_columns == columns_amount:
            return
        for _ in self.__card_list:
            try:
                _.grid_forget()
            except:
                pass

        for card_number in range(0,len(self.__card_list)):
            self.__card_list[card_number].grid(row=int(card_number//columns_amount), column=int(card_number % columns_amount))

    def place_configure(self, **kw):

        super().place_configure(kw)
        self.update_content()



