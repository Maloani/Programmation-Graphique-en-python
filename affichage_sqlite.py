from tkinter import END, ttk

from flask import app
table = ttk.Treeview(app, columns=("Nom","Email"),
show="headings")
table.heading("Nom", text="Nom")
table.heading("Email", text="Email")
table.pack()
table.insert("", END, values=("Jean","jeanmarie@gmail.com"))