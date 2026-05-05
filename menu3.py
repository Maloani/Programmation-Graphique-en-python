from tkinter import *
app = Tk()
app.title("Interface Moderne Python DABIRE")
app.geometry("900x550")
app.configure(bg="#F1F5F9")
sidebar = Frame(app, bg="#0F172A", width=220)
sidebar.pack(side=LEFT, fill=Y)
main = Frame(app, bg="#F1F5F9")
main.pack(side=RIGHT, fill=BOTH, expand=True)
Label(
 sidebar,
 text="PYTHON GUI",
 bg="#0F172A",
 fg="white",
 font=("Arial", 18, "bold")
).pack(pady=30)
menu_items = [
 "🏠 Tableau de bord",
 "👤 Utilisateurs",
 "📦 Produits",
 "🧾 Commandes",
 "📊 Statistiques",
 "⚙ Paramètres"
]
for item in menu_items:
 Button(
 sidebar,
 text=item,
 bg="#1E293B",
 fg="white",
 activebackground="#2563EB",
 activeforeground="white",
 font=("Arial", 11),
 relief=FLAT,
 anchor="w",
 padx=20,
 pady=10
 ).pack(fill=X, padx=12, pady=4)
header = Frame(main, bg="white", height=70)
header.pack(fill=X)
Label(
 header,
 text="Dashboard Administrateur",
 bg="white",
 fg="#0F172A",
 font=("Arial", 20, "bold")
).pack(side=LEFT, padx=30, pady=18)
cards = Frame(main, bg="#F1F5F9")
cards.pack(fill=X, padx=30, pady=30)
for title, value in [
 ("Étudiants", "50"),
 ("Produits", "5"),
 ("Commandes", "20"),
 ("Revenus", "400 USD")
]:
 card = Frame(cards, bg="white", width=160, height=100)
 card.pack(side=LEFT, padx=10)
 card.pack_propagate(False)
 Label(card, text=title, bg="white", fg="#64748B", font=("Arial",
11)).pack(pady=10)
 Label(card, text=value, bg="white", fg="#2563EB",
font=("Arial", 18, "bold")).pack()
app.mainloop()
