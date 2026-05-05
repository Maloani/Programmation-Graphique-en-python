from tkinter import *
app = Tk()
app.title("Dashboard Moderne")
app.geometry("800x500")
sidebar = Frame(app, bg="#0F172A", width=200)
sidebar.pack(side=LEFT, fill=Y)
content = Frame(app, bg="#F1F5F9")
content.pack(side=RIGHT, fill=BOTH, expand=True)
Label( sidebar,text="MS APP",bg="#0F172A",fg="white",font=("Arial", 18, "bold")).pack(pady=30)
menus = ["🏠 Accueil", "👥 Clients", "📦 Produits", "🧾Commandes", "⚙ Paramètres"]
for item in menus:
 Button(sidebar,text=item,bg="#575152",fg="white",font=("Arial", 12),relief=FLAT,anchor="w",padx=20
 ).pack(fill=X, padx=15, pady=5)
Label(
 content,
 text="Bienvenue dans le Dashboard",
 bg="#F1F5F9",
 fg="#0F172A",
 font=("Arial", 24, "bold")
).pack(pady=80)
app.mainloop()