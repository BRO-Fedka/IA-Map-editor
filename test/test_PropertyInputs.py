from tkinter import *
from GUI.PropertyInputs.CharPI import CharPI
from GUI.PropertyInputs.DirectionPI import DirectionPI
from GUI.PropertyInputs.PositiveFloatPI import PositiveFloatPI
tk = Tk()
CharInput = CharPI(tk, lambda: 'A', lambda e: print(e))
CharInput.pack()
DirInput = DirectionPI(tk, lambda: 5, lambda e: print(e))
DirInput.pack()
DirInput = PositiveFloatPI(tk, lambda: 0.5, lambda e: print(e))
DirInput.pack()
tk.mainloop()