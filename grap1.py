from tkinter import *
app = Tk()
app.geometry("300x300")
Label(app,text="Nom").pack()
Entry(app).pack()
Label(app,text="Pays").pack()
from tkinter import ttk
ttk.Combobox(app, values=["NIGER","Canada","Burkina faso"]).pack()
Checkbutton(app,text="J'accepte").pack()
Button(app,text="Envoyer").pack()
app.mainloop()