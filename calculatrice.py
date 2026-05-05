# calculatrice_graphique.py

import tkinter as tk
from tkinter import messagebox


class Calculatrice:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculatrice Graphique en Python")
        self.root.geometry("380x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")

        self.expression = ""

        self.ecran = tk.Entry(
            root,
            font=("Arial", 24, "bold"),
            bg="#ffffff",
            fg="#000000",
            bd=0,
            justify="right"
        )
        self.ecran.pack(fill="both", padx=15, pady=20, ipady=18)

        self.creer_boutons()

    def cliquer(self, valeur):
        self.expression += str(valeur)
        self.ecran.delete(0, tk.END)
        self.ecran.insert(tk.END, self.expression)

    def effacer(self):
        self.expression = ""
        self.ecran.delete(0, tk.END)

    def supprimer_un(self):
        self.expression = self.expression[:-1]
        self.ecran.delete(0, tk.END)
        self.ecran.insert(tk.END, self.expression)

    def calculer(self):
        try:
            if self.expression == "":
                return

            resultat = eval(self.expression)
            self.ecran.delete(0, tk.END)
            self.ecran.insert(tk.END, str(resultat))
            self.expression = str(resultat)

        except ZeroDivisionError:
            messagebox.showerror("Erreur", "Division par zéro impossible")
            self.effacer()

        except Exception:
            messagebox.showerror("Erreur", "Expression invalide")
            self.effacer()

    def creer_boutons(self):
        cadre = tk.Frame(self.root, bg="#1e1e1e")
        cadre.pack()

        boutons = [
            ["C", "⌫", "%", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["0", ".", "=", ""]
        ]

        for ligne in range(len(boutons)):
            for colonne in range(len(boutons[ligne])):
                texte = boutons[ligne][colonne]

                if texte == "":
                    continue

                couleur = "#333333"
                couleur_texte = "#ffffff"

                if texte in ["/", "*", "-", "+", "%", "="]:
                    couleur = "#ff9500"

                if texte in ["C", "⌫"]:
                    couleur = "#b22222"

                bouton = tk.Button(
                    cadre,
                    text=texte,
                    font=("Arial", 18, "bold"),
                    width=5,
                    height=2,
                    bg=couleur,
                    fg=couleur_texte,
                    bd=0,
                    activebackground="#555555",
                    activeforeground="#ffffff",
                    command=lambda x=texte: self.action_bouton(x)
                )

                if texte == "=":
                    bouton.grid(
                        row=ligne,
                        column=colonne,
                        columnspan=2,
                        padx=5,
                        pady=5,
                        sticky="nsew"
                    )
                else:
                    bouton.grid(
                        row=ligne,
                        column=colonne,
                        padx=5,
                        pady=5,
                        sticky="nsew"
                    )

    def action_bouton(self, valeur):
        if valeur == "C":
            self.effacer()
        elif valeur == "⌫":
            self.supprimer_un()
        elif valeur == "=":
            self.calculer()
        else:
            self.cliquer(valeur)


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculatrice(root)
    root.mainloop()