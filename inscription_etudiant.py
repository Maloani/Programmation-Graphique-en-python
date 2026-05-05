from tkinter import *
from tkinter import messagebox
def inscrire():
    nom = entry_nom.get()
    postnom = entry_postnom.get()
    email = entry_email.get()
    option = entry_option.get()
    if nom == "" or postnom == "" or email == "" or option == "":
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
    else:
        messagebox.showinfo("Succès", f"Étudiant inscrit : {nom} {postnom}")
app = Tk()
app.title("Formulaire d'inscription étudiant")
app.geometry("400x350")
Label(app, text="INSCRIPTION ÉTUDIANT", font=("Arial", 16,
"bold")).pack(pady=10)
Label(app, text="Nom").pack()
entry_nom = Entry(app, width=35)
entry_nom.pack()
Label(app, text="Postnom").pack()
entry_postnom = Entry(app, width=35)
entry_postnom.pack()
Label(app, text="Email").pack()
entry_email = Entry(app, width=35)
entry_email.pack()
Label(app, text="Option").pack()
entry_option = Entry(app, width=35)
entry_option.pack()
Button(app, text="Inscrire", bg="green", fg="white",
command=inscrire).pack(pady=20)
app.mainloop()