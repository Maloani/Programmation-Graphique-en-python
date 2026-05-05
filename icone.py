from tkinter import *
app = Tk()
app.geometry("600x400")
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=3)
app.grid_rowconfigure(0, weight=1)
sidebar = Frame(app, bg="#0F172A")
sidebar.grid(row=0, column=0, sticky="nsew")
content = Frame(app, bg="#F1F5F9")
content.grid(row=0, column=1, sticky="nsew")
Label(sidebar, text="MENU", bg="#0F172A",
fg="white").pack(pady=20)
Label(content, text="Contenu principal", bg="#F1F5F9",
font=("Arial", 20)).pack(pady=50)
app.mainloop()