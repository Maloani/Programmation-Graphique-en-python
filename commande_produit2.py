from tkinter import *
from tkinter import ttk, messagebox
prix_produits = {
 "Ordinateur": 500,
 "Téléphone": 250,
 "Clavier": 20,
 "Souris": 10
}
def commander():
 produit = combo_produit.get()
 quantite = entry_quantite.get()
 if produit == "" or quantite == "":
    messagebox.showerror("Erreur", "Veuillez choisir un produit et entrer la quantité")
 else:
    quantite = int(quantite)
    prix = prix_produits[produit]
    total = prix * quantite
    table.insert("", END, values=(produit, quantite, prix, total))
    label_total.config(text=f"Total : {total} USD")
app = Tk()
app.title("Commande Produit")
app.geometry("650x420")
Label(app, text="SYSTÈME DE COMMANDE", font=("Arial", 18,
"bold")).pack(pady=10)
frame = Frame(app)
frame.pack()
Label(frame, text="Produit").grid(row=0, column=0)
combo_produit = ttk.Combobox(frame,
values=list(prix_produits.keys()))
combo_produit.grid(row=0, column=1)
Label(frame, text="Quantité").grid(row=1, column=0)
entry_quantite = Entry(frame)
entry_quantite.grid(row=1, column=1)
Button(app, text="Commander", bg="blue", fg="white",
command=commander).pack(pady=10)
table = ttk.Treeview(app, columns=("Produit", "Quantité", "Prix",
"Total"), show="headings")
for col in ("Produit", "Quantité", "Prix", "Total"):
 table.heading(col, text=col)
table.pack(fill=BOTH, expand=True, padx=20, pady=20)
label_total = Label(app, text="Total : 0 USD", font=("Arial", 14,
"bold"))
label_total.pack()
app.mainloop()