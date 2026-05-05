from tkinter import *
from tkinter import messagebox
session = {}
users = { "admin": { "password": "1234","role": "ADMIN"}, "agent": { "password": "0000", "role": "AGENT"}
}
def ouvrir_admin():
 fen = Toplevel(app)
 fen.title("Dashboard Admin")
 fen.geometry("400x250")
 Label(fen, text="Bienvenue ADMIN", font=("Arial", 18,"bold")).pack(pady=40)
def ouvrir_agent():
 fen = Toplevel(app)
 fen.title("Dashboard Agent")
 fen.geometry("400x250")
 Label(fen, text="Bienvenue AGENT", font=("Arial", 18,"bold")).pack(pady=40)
def login():
 username = entry_user.get()
 password = entry_pass.get()
 if username in users and users[username]["password"] == password: session["username"] = username
 session["role"] = users[username]["role"]
 messagebox.showinfo("Succès", f"Bienvenue {username}")
 if session["role"] == "ADMIN": ouvrir_admin()
 elif session["role"] == "AGENT": ouvrir_agent()
 else:
    messagebox.showerror("Erreur", "Identifiants incorrects")
app = Tk()
app.title("Login sécurisé")
app.geometry("380x300")
Label(app, text="CONNEXION", font=("Arial", 18,
"bold")).pack(pady=20)
Label(app, text="Nom utilisateur").pack()
entry_user = Entry(app, width=30)
entry_user.pack(pady=5)
Label(app, text="Mot de passe").pack()
entry_pass = Entry(app, width=30, show="*")
entry_pass.pack(pady=5)
Button(app, text="Connexion", bg="#2563EB", fg="white",
command=login).pack(pady=20)
app.mainloop()