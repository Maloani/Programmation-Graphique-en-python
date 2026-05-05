from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
conn = sqlite3.connect("pharmacie.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS medicaments(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 nom TEXT,
 prix REAL,
 quantite INTEGER
)
""")
conn.commit()
def afficher():
    table.delete(*table.get_children())
    cursor.execute("SELECT * FROM medicaments")
    for row in cursor.fetchall():
        table.insert("", END, values=row)

def ajouter():
    nom = entry_nom.get()
    prix = entry_prix.get()
    quantite = entry_quantite.get()
    if nom == "" or prix == "" or quantite == "":
        messagebox.showerror("Erreur", "Champs obligatoires")
    else:
        cursor.execute("INSERT INTO medicaments(nom, prix, quantite) VALUES(?,?,?)", (nom, prix, quantite))
        conn.commit()
        afficher()

def alerte_stock():
    cursor.execute("SELECT nom, quantite FROM medicaments WHERE quantite <= 5")
    produits = cursor.fetchall()
    if produits:
        message = ""
        for p in produits:
            message += f"{p[0]} : {p[1]} restant(s)\n"
        messagebox.showwarning("Stock faible", message)
    else:
        messagebox.showinfo("Stock", "Aucun stock faible")

app = Tk()
app.title("Pharmacie - Gestion Stock")
app.geometry("700x450")
Label(app, text="GESTION PHARMACIE", font=("Arial", 18,
"bold")).pack(pady=10)
frame = Frame(app)
frame.pack()
Label(frame, text="Médicament").grid(row=0, column=0)
entry_nom = Entry(frame)
entry_nom.grid(row=0, column=1)
Label(frame, text="Prix").grid(row=1, column=0)
entry_prix = Entry(frame)
entry_prix.grid(row=1, column=1)
Label(frame, text="Quantité").grid(row=2, column=0)
entry_quantite = Entry(frame)
entry_quantite.grid(row=2, column=1)
Button(app, text="Ajouter médicament", bg="green", fg="white",
command=ajouter).pack(pady=10)
Button(app, text="Alerte stock faible", bg="orange", fg="black",
command=alerte_stock).pack()
table = ttk.Treeview(app, columns=("ID", "Nom", "Prix",
"Quantité"), show="headings")
for col in ("ID", "Nom", "Prix", "Quantité"):
 table.heading(col, text=col)
table.pack(fill=BOTH, expand=True, padx=20, pady=20)
afficher()
app.mainloop()