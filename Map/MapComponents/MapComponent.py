from tkinter import *
from GUI.Workspace import *
from Map.Map import *


class MapComponent:
    __workspace: Workspace = None
    __map: Map = None

    def __init__(self, map: Map, workspace: Workspace):
        self.__workspace = workspace
        self.__map = map

    @staticmethod
    def get_card_icon() -> PhotoImage:
        return PhotoImage(file="src/empty.png")
