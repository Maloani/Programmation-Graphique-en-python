from tkinter import *
from tkinter import messagebox
def login():
 username = entry_user.get()
 password = entry_pass.get()
 if username == "admin" and password == "1234":
    messagebox.showinfo("Succès", "Connexion réussie")
 else:
    messagebox.showerror("Erreur", "Nom d'utilisateur ou mot de passe incorrect")
app = Tk()
app.title("Connexion utilisateur")
app.geometry("550x380")
Label(app, text="LOGIN UTILISATEUR", font=("Arial", 20, "bold")).pack(pady=15)
Label(app, text="Nom d'utilisateur").pack()
entry_user = Entry(app, width=30)
entry_user.pack()
Label(app, text="Mot de passe").pack()
entry_pass = Entry(app, width=30, show="*")
entry_pass.pack()
Button(app, text="Connexion", bg="blue", fg="white", command=login).pack(pady=20)
app.mainloop()