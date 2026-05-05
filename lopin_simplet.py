from tkinter import *
from tkinter import messagebox
def login():
 username = entry_user.get()
 password = entry_pass.get()
 if username == "admin" and password == "1234":
    messagebox.showinfo("Succès", "Connexion réussie")
 else:
    messagebox.showerror("Erreur", "Identifiants incorrects")
app = Tk()
app.title("Login")
app.geometry("350x250")
Label(app, text="Nom utilisateur").pack()
entry_user = Entry(app)
entry_user.pack()
Label(app, text="Mot de passe").pack()
entry_pass = Entry(app, show="*")
entry_pass.pack()
Button(app, text="Connexion", command=login).pack(pady=20)
app.mainloop()
