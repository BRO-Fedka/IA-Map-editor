import logging
from tkinter import *
from GUI.ICommon import *


class PreviewForm(Toplevel, ICommon):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        if self.get_workspace().get_map() is None:
            self.destroy()
            return
        self.attributes('-toolwindow', True)
        self.resizable(False, False)
        self['bg'] = "#ddd"
        self.title('Preview')
        self.focus()
        self.__lbl_wh = Label(self, text='WH:', bg=self['bg'])
        self.__lbl_wh.grid(row=0, column=0, pady=5, padx=5)
        self.__lbl_blur = Label(self, text='Blur:', bg=self['bg'])
        self.__lbl_blur.grid(row=1, column=0, pady=5, padx=5)
        self.__txt_wh = Entry(self)
        self.__txt_wh.grid(row=0, column=1, padx=5)
        self.__txt_wh.insert(0,"640")
        self.__blur_var = BooleanVar()
        self.__blur_var.set(False)
        self.__chk_blur = Checkbutton(self, bg=self['bg'], variable=self.__blur_var, onvalue=True, offvalue=False, )
        self.__chk_blur.grid(row=1, column=1, sticky=W)
        self.__btn_generate = Button(self, text="Generate", command=self.generate)
        self.__btn_generate.grid(row=2, column=0, columnspan=2, sticky=EW, pady=5, padx=5)
        self.bind("<FocusOut>", self.__focus_out)

    def __focus_out(self, event=None):
        self.destroy()

    def generate(self):
        try:
            self.get_workspace().get_map().get_preview_image_draw(int(self.__txt_wh.get()), self.__blur_var.get())
            self.destroy()
        except:
            logging.exception('')
