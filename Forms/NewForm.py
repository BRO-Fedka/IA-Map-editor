from tkinter import *
from GUI.ICommon import *
from tkinter.messagebox import showwarning
from GUI.SelectButton import *
from Map.Map import *
import os
import logging

class NewForm(Toplevel, ICommon):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        if not self.get_workspace().get_map() is None:
            showwarning(title="One moment ...", message="Have you saved your map ?")
        self.attributes('-toolwindow', True)
        self.resizable(False, False)
        self['bg'] = "#ddd"
        self.title('New')
        self.focus()
        self.__lbl_wh = Label(self, text='WH:', bg=self['bg'])
        self.__lbl_wh.grid(row=0, column=0, pady=5, padx=5)
        self.__lbl_ct = Label(self, text='CT:', bg=self['bg'])
        self.__lbl_ct.grid(row=1, column=0, pady=5, padx=5)
        self.__txt_wh = Entry(self)
        self.__txt_wh.grid(row=0, column=1, padx=5)
        self.__txt_wh.insert(0,"16")
        self.__cbx_ct = SelectButton(self, vals=os.listdir('CTs'),default='default.json')
        self.__cbx_ct.grid(row=1, column=1, sticky=EW, padx=5)
        self.__btn_new = Button(self, text="New", command=self.new)
        self.__btn_new.grid(row=2, column=0, columnspan=2, sticky=EW, pady=5, padx=5)
        self.bind("<FocusOut>", self.__focus_out)

    def __focus_out(self, event=None):
        self.destroy()

    def new(self):
        try:
            self.master.get_workspace().set_map(Map.new_map(int(self.__txt_wh.get()), 'CTs\\'+self.__cbx_ct.get(),  self.master.get_workspace()))
            self.destroy()
        except:
            logging.exception('')
