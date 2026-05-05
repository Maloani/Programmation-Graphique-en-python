from tkinter import *
from tkinter import messagebox
def afficher_devise():
 devise = choix_devise.get()
 if devise == "":
    messagebox.showerror("Erreur", "Veuillez choisir une devise")
 else:
    messagebox.showinfo("Devise sélectionnée", f"Vous avez choisi : {devise}")
app = Tk()
app.title("Sélection devise")
app.geometry("450x350")
Label(app, text="CHOISIR UNE DEVISE", font=("Arial", 30, "bold")).pack(pady=15)
choix_devise = StringVar()
Radiobutton(app, text="USD - Dollar américain", variable=choix_devise,
value="USD").pack()
Radiobutton(app, text="CDF - Franc congolais", variable=choix_devise,
value="CDF").pack()
Radiobutton(app, text="FCFA - Franc CFA", variable=choix_devise,
value="FCFA").pack()
Radiobutton(app, text="UGX - Ugandan shillings", variable=choix_devise,
value="UGX").pack()
Button(app, text="Valider", bg="darkred", fg="white", command=afficher_devise).pack(pady=20)
app.mainloop()