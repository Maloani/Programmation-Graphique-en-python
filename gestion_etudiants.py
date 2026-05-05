from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
conn = sqlite3.connect("etudiants.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS etudiants(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nom TEXT,
 email TEXT,
 option TEXT
)
""")
conn.commit()
def afficher():
 table.delete(*table.get_children())
 cursor.execute("SELECT * FROM etudiants")
 for row in cursor.fetchall(): table.insert("", END, values=row)
def ajouter():
    nom = entry_nom.get()
    email = entry_email.get()
    option = entry_option.get()
    if nom == "" or email == "" or option == "":
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
    else:
        cursor.execute("INSERT INTO etudiants(nom,email,option) VALUES(?,?,?)", (nom, email, option))
        conn.commit()
        afficher()
        entry_nom.delete(0, END)
        entry_email.delete(0, END)
        entry_option.delete(0, END)

def supprimer():
 selected = table.selection()
 if selected:
    id_etudiant = table.item(selected)["values"][0]
    cursor.execute("DELETE FROM etudiants WHERE id=?",
(id_etudiant,))
    conn.commit()
    afficher()
 else:
    messagebox.showerror("Erreur", "Sélectionnez un étudiant")
app = Tk()
app.title("Gestion des étudiants")
app.geometry("700x450")
Label(app, text="GESTION DES ÉTUDIANTS", font=("Arial", 18,
"bold")).pack(pady=10)
frame = Frame(app)
frame.pack()
Label(frame, text="Nom").grid(row=0, column=0)
entry_nom = Entry(frame)
entry_nom.grid(row=0, column=1)
Label(frame, text="Email").grid(row=1, column=0)
entry_email = Entry(frame)
entry_email.grid(row=1, column=1)
Label(frame, text="Option").grid(row=2, column=0)
entry_option = Entry(frame)
entry_option.grid(row=2, column=1)
Button(app, text="Ajouter", bg="green", fg="white",
command=ajouter).pack(pady=10)
Button(app, text="Supprimer", bg="red", fg="white",
command=supprimer).pack()
table = ttk.Treeview(app, columns=("ID", "Nom", "Email",
"Option"), show="headings")
for col in ("ID", "Nom", "Email", "Option"):
 table.heading(col, text=col)
table.pack(fill=BOTH, expand=True, padx=20, pady=20)
afficher()
app.mainloop()