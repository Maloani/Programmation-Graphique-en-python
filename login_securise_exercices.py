from tkinter import *
from tkinter import messagebox
import random
users = {
 "admin": { "password": "1234", "role": "ADMIN" },"agent": { "password": "0000", "role": "AGENT"
 }
}
tentatives = 0
otp_code = ""
def ouvrir_dashboard_admin():
 admin = Toplevel(app)
 admin.title("Dashboard Admin")
 admin.geometry("450x300")
 admin.configure(bg="#0F172A")
 Label( admin, text="Bienvenue Admin", bg="#0F172A", fg="white", font=("Arial", 20, "bold") ).pack(pady=40)
 Label( admin, text="Vous avez accès à toutes les fonctionnalités.", bg="#0F172A",fg="white",font=("Arial", 12)
 ).pack()
def ouvrir_dashboard_agent():
 agent = Toplevel(app)
 agent.title("Dashboard Agent")
 agent.geometry("450x300")
 agent.configure(bg="#F1F5F9")
 Label( agent, text="Bienvenue Agent", bg="#F1F5F9",fg="#0F172A", font=("Arial", 20, "bold") ).pack(pady=40)
 Label( agent, text="Vous avez accès aux tâches des agents.", bg="#F1F5F9", fg="#0F172A", font=("Arial", 12)
 ).pack()
def generer_otp():
 global otp_code
 otp_code = str(random.randint(1000, 9999))
 messagebox.showinfo("OTP généré", f"Votre code OTP est :{otp_code}")
def verifier_login():
 global tentatives
 username = entry_user.get()
 password = entry_pass.get()
 otp = entry_otp.get()
 if tentatives >= 3:
    messagebox.showerror("Compte bloqué", "Vous avez dépassé 3 tentatives.") 
    return
 if username == "" or password == "" or otp == "":
    messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
    return
 if otp != otp_code:
    tentatives += 1
    messagebox.showerror("Erreur OTP", f"Code OTP incorrect. Tentative {tentatives}/3")
    return
 if username in users and users[username]["password"] == password:
    role = users[username]["role"]
    messagebox.showinfo("Succès", f"Connexion réussie comme {role}")
    if role == "ADMIN":
        ouvrir_dashboard_admin()
    elif role == "AGENT":
        ouvrir_dashboard_agent()
 else:
    tentatives += 1
    messagebox.showerror("Erreur", f"Identifiants incorrects. Tentative {tentatives}/3")
    if tentatives >= 3:
        btn_login.config(state=DISABLED)
        messagebox.showerror("Bloqué", "Connexion bloquée après 3 tentatives.")
app = Tk()
app.title("Login sécurisé avec OTP")
app.geometry("420x420")
app.configure(bg="#F1F5F9")
Label(
 app,
 text="CONNEXION SÉCURISÉE",
 bg="#F1F5F9",
 fg="#0F172A",
 font=("Arial", 18, "bold")
).pack(pady=20)
Label(app, text="Nom utilisateur", bg="#F1F5F9").pack()
entry_user = Entry(app, width=35)
entry_user.pack(pady=5)
Label(app, text="Mot de passe", bg="#F1F5F9").pack()
entry_pass = Entry(app, width=35, show="*")
entry_pass.pack(pady=5)
Button(
 app,
 text="Générer OTP",
 bg="#16A34A",
 fg="white",
 font=("Arial", 11, "bold"),
 command=generer_otp
).pack(pady=15)
Label(app, text="Code OTP", bg="#F1F5F9").pack()
entry_otp = Entry(app, width=35)
entry_otp.pack(pady=5)
btn_login = Button(
 app,
 text="Connexion",
 bg="#2563EB",
 fg="white",
 font=("Arial", 12, "bold"),
 command=verifier_login
)
btn_login.pack(pady=20)
Label(
 app,
 text="Comptes test : admin/1234 ou agent/0000",
 bg="#F1F5F9",
 fg="#64748B",
 font=("Arial", 10)
).pack(pady=10)
app.mainloop()