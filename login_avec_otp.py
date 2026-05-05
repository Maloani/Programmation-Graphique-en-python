from tkinter import *
from tkinter import messagebox
import random
otp_code = ""
def envoyer_otp():
 global otp_code
 otp_code = str(random.randint(100000, 999999))
 messagebox.showinfo("OTP envoyé", f"Votre code OTP est :{otp_code}")
def verifier_otp():
 code = entry_otp.get()
 if code == otp_code:
    messagebox.showinfo("Succès", "Connexion confirmée")
 else:
    messagebox.showerror("Erreur", "Code OTP incorrect")
app = Tk()
app.title("Vérification OTP")
app.geometry("350x250")
Label(app, text="VÉRIFICATION OTP", font=("Arial", 16,
"bold")).pack(pady=20)
Button(app, text="Envoyer OTP",
command=envoyer_otp).pack(pady=10)
Label(app, text="Entrer le code OTP").pack()
entry_otp = Entry(app, width=30)
entry_otp.pack(pady=5)
Button(app, text="Vérifier", bg="green", fg="white",
command=verifier_otp).pack(pady=20)
app.mainloop()