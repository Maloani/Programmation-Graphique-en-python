from tkinter import *
from tkinter import messagebox
import sqlite3
conn = sqlite3.connect("ecole.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS etudiants(
id INTEGER PRIMARY KEY AUTOINCREMENT,
nom TEXT,
email TEXT
)
""")
conn.commit()
def enregistrer():
 nom = entry_nom.get()
 email = entry_email.get()
 cursor.execute(
 "INSERT INTO etudiants(nom,email) VALUES(?,?)",
 (nom,email)
 )
 conn.commit()
 messagebox.showinfo("Succès", "Étudiant enregistré")
app = Tk()
app.title("Gestion Étudiant")
app.geometry("400x300")
Label(app, text="Nom").pack()
entry_nom = Entry(app, width=30)
entry_nom.pack()
Label(app, text="Email").pack()
entry_email = Entry(app, width=30)
entry_email.pack()
Button(
 app,
 text="Enregistrer",
 bg="green",
 fg="white",
 command=enregistrer
).pack(pady=20)
app.mainloop()