from tkinter import *
from tkinter import ttk, messagebox
def calculer_commande():
 produit = combo_produit.get()
 quantite = entry_quantite.get()
 prix = {
 "Ordinateur": 500,
 "Téléphone": 250,
 "Clavier": 20,
 "Souris": 10
 }
 if produit == "" or quantite == "":
    messagebox.showerror("Erreur", "Veuillez choisir un produit et entrer la quantité")
 else:
    quantite = int(quantite)
 total = prix[produit] * quantite
 table.insert("", END, values=(produit, quantite, prix[produit], total))
 label_total.config(text=f"Total à payer : {total} USD")
app = Tk()
app.title("Système de commande produit")
app.geometry("650x450")
Label(app, text="COMMANDE PRODUIT", font=("Arial", 16,
"bold")).pack(pady=10)
frame = Frame(app)
frame.pack(pady=10)
Label(frame, text="Produit").grid(row=0, column=0)
combo_produit = ttk.Combobox(frame, values=["Ordinateur", "Téléphone",
"Clavier", "Souris"])
combo_produit.grid(row=0, column=1)
Label(frame, text="Quantité").grid(row=1, column=0)
entry_quantite = Entry(frame)
entry_quantite.grid(row=1, column=1)
Button(app, text="Commander", bg="blue", fg="white",
command=calculer_commande).pack(pady=10)
table = ttk.Treeview(app, columns=("Produit", "Quantité", "Prix", "Total"),
show="headings")
table.heading("Produit", text="Produit")
table.heading("Quantité", text="Quantité")
table.heading("Prix", text="Prix unitaire")
table.heading("Total", text="Total")
table.pack(fill=BOTH, expand=True, padx=20, pady=10)
label_total = Label(app, text="Total à payer : 0 USD", font=("Arial", 14,
"bold"))
label_total.pack(pady=10)
app.mainloop()
