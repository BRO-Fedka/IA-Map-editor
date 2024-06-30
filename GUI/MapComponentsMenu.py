from tkinter import *
from typing import *
from GUI.MapComponentCard import *
from GUI.ICommon import *


class MapComponentsMenu(Frame, ICommon):
    __card_list: List[MapComponentCard] = []
    __last_amount_of_columns: int = 0
    __last_amount_of_cards: int = 0
    __selected_card: MapComponentCard = None

    def __init__(self, master: Optional[Misc], **kwargs):
        super().__init__(master, kwargs)

    def add_card(self, card: MapComponentCard):
        if self.__selected_card is None:
            self.__selected_card = card
            card.select()
        self.__last_amount_of_cards = len(self.__card_list)
        self.__card_list.append(card)
        self.update_content()

    def update_content(self):
        columns_amount = self.winfo_width() // 110
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
            self.__card_list[card_number].grid(row=int(card_number//columns_amount), column=int(card_number % columns_amount), padx=5, pady=5)

    def place_configure(self, **kw):

        super().place_configure(kw)
        self.update_content()

    def select(self, card: MapComponentCard):
        self.get_selected_map_component().remove_all_selections()
        self.__selected_card = card
        children = self.winfo_children()
        for child in children:
            if child != card:
                child.unselect()
        card.select()

    def get_selected_map_component(self) -> Type[MapComponent]:
        return self.__selected_card.get_map_component()




