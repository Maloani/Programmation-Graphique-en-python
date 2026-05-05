from tkinter import *
from tkinter import ttk, messagebox
produits = {
 "Riz": 10,
 "Huile": 5,
 "Sucre": 3,
 "Farine": 4,
 "Savon": 2
}
total_general = 0
def ajouter_panier():
 global total_general
 produit = combo_produit.get()
 quantite = entry_quantite.get()
 if produit == "" or quantite == "":
    messagebox.showerror("Erreur", "Veuillez choisir un produit et saisir la quantité")
    return
 quantite = int(quantite)
 prix = produits[produit]
 total = prix * quantite
 total_general += total
 table.insert("", END, values=(produit, quantite, prix, total))
 label_total.config(text=f"Total général : {total_general} USD")
def payer():
 messagebox.showinfo("Paiement", f"Paiement effectué : {total_general} USD")
app = Tk()
app.title("Mini POS")
app.geometry("700x500")
Label(app, text="MINI SYSTÈME DE CAISSE POS", font=("Arial",
18, "bold")).pack(pady=10)
frame = Frame(app)
frame.pack(pady=10)
Label(frame, text="Produit").grid(row=0, column=0)
combo_produit = ttk.Combobox(frame,
values=list(produits.keys()))
combo_produit.grid(row=0, column=1)
Label(frame, text="Quantité").grid(row=1, column=0)
entry_quantite = Entry(frame)
entry_quantite.grid(row=1, column=1)
Button(app, text="Ajouter au panier", bg="green", fg="white",
command=ajouter_panier).pack(pady=10)
table = ttk.Treeview(app, columns=("Produit", "Quantité", "Prix",
"Total"), show="headings")
for col in ("Produit", "Quantité", "Prix", "Total"):
 table.heading(col, text=col)
table.pack(fill=BOTH, expand=True, padx=20, pady=20)
label_total = Label(app, text="Total général : 0 USD",
font=("Arial", 15, "bold"))
label_total.pack(pady=10)
Button(app, text="Payer", bg="blue", fg="white", font=("Arial",
12, "bold"), command=payer).pack()
app.mainloop()