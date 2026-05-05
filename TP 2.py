# -*- coding: utf-8 -*-

# Importation de toutes les classes et fonctions de base de tkinter
from tkinter import *
# Importation des widgets thématisés ttk (plus modernes) et de la boîte de message
from tkinter import ttk, messagebox
# Import du module font pour personnaliser les polices de caractères
from tkinter import font as tkfont


class DepenseApp:
    """Application de gestion des dépenses personnelles avec interface améliorée."""

    def __init__(self, root):
        """
        Constructeur : initialise la fenêtre principale, les variables,
        crée les widgets et applique le style.
        """
        self.root = root
        # Titre de la fenêtre
        self.root.title("💰 Gestion des Dépenses")
        # Dimensions de la fenêtre (largeur x hauteur)
        self.root.geometry("850x600")
        # Empêcher le redimensionnement pour garder un design maîtrisé (optionnel)
        self.root.resizable(True, True)
        # Couleur de fond générale de la fenêtre
        self.root.configure(bg='#f0f0f5')

        # Variables de suivi
        self.total = 0.0          # Total des dépenses ajoutées
        self.budget = 1000.0      # Budget maximal autorisé

        # ----- Configuration du style ttk pour un affichage moderne -----
        self.style = ttk.Style()
        # Choix d'un thème disponible ('clam', 'alt', 'default', 'classic')
        self.style.theme_use('clam')
        # Personnalisation des boutons
        self.style.configure('TButton',
                             font=('Segoe UI', 10, 'bold'),
                             padding=8,
                             background='#4a7abc',
                             foreground='white')
        self.style.map('TButton',
                       background=[('active', '#3a5f8c')])
        # Personnalisation des labels ttk
        self.style.configure('TLabel',
                             font=('Segoe UI', 10),
                             background='#f0f0f5')
        # Personnalisation de l'entrée ttk
        self.style.configure('TEntry',
                             padding=6)
        # Personnalisation du Treeview
        self.style.configure('Treeview',
                             font=('Segoe UI', 10),
                             rowheight=25)
        self.style.configure('Treeview.Heading',
                             font=('Segoe UI', 10, 'bold'))

        # ----- Création du titre principal -----
        titre_font = tkfont.Font(family='Segoe UI', size=18, weight='bold')
        titre = Label(root, text="Suivi des Dépenses Quotidiennes",
                      font=titre_font, bg='#f0f0f5', fg='#2c3e50')
        titre.grid(row=0, column=0, columnspan=3, pady=(20, 10))

        # ----- Cadre du formulaire de saisie (avec contour visuel) -----
        cadre_saisie = LabelFrame(root, text=" Nouvelle dépense ",
                                  font=('Segoe UI', 11, 'bold'),
                                  bg='#e8edf2', fg='#2c3e50',
                                  padx=15, pady=15)
        cadre_saisie.grid(row=1, column=0, padx=20, pady=10, sticky="ew", columnspan=3)

        # Label + champ Description
        Label(cadre_saisie, text="Description :",
              bg='#e8edf2', font=('Segoe UI', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.desc = ttk.Entry(cadre_saisie, width=30, font=('Segoe UI', 10))
        self.desc.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

        # Label + champ Montant
        Label(cadre_saisie, text="Montant (€) :",
              bg='#e8edf2', font=('Segoe UI', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.montant = ttk.Entry(cadre_saisie, width=30, font=('Segoe UI', 10))
        self.montant.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

        # Label + liste déroulante Catégorie
        Label(cadre_saisie, text="Catégorie :",
              bg='#e8edf2', font=('Segoe UI', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.cat = ttk.Combobox(cadre_saisie,
                                values=["Transport", "Nourriture", "Santé", "Loisirs", "Logement", "Autres"],
                                font=('Segoe UI', 10), state='readonly')
        self.cat.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
        self.cat.current(0)  # Sélection par défaut : premier élément

        # Bouton d'ajout dans le cadre
        self.bouton_ajouter = ttk.Button(cadre_saisie, text="➕ Ajouter la dépense",
                                         command=self.ajouter)
        self.bouton_ajouter.grid(row=3, column=0, columnspan=2, pady=15)

        # ----- Cadre du tableau des dépenses -----
        cadre_tableau = LabelFrame(root, text=" Historique des dépenses ",
                                   font=('Segoe UI', 11, 'bold'),
                                   bg='#f0f0f5', fg='#2c3e50',
                                   padx=10, pady=10)
        cadre_tableau.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")

        # Définition des colonnes du tableau (Treeview)
        colonnes = ("Desc", "Montant", "Cat")
        self.table = ttk.Treeview(cadre_tableau, columns=colonnes, show="headings",
                                  selectmode='browse', height=8)
        # En-têtes des colonnes avec texte et largeur
        self.table.heading("Desc", text="Description")
        self.table.column("Desc", width=300, anchor='center')
        self.table.heading("Montant", text="Montant (€)")
        self.table.column("Montant", width=150, anchor='center')
        self.table.heading("Cat", text="Catégorie")
        self.table.column("Cat", width=200, anchor='center')
        # Placement du tableau avec possibilité d'expansion
        self.table.pack(fill=BOTH, expand=True, padx=5, pady=5)

        # Barre de défilement verticale pour le tableau
        scrollbar = ttk.Scrollbar(cadre_tableau, orient=VERTICAL, command=self.table.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.table.configure(yscrollcommand=scrollbar.set)

        # ----- Zone d'affichage du total et du budget restant -----
        cadre_budget = Frame(root, bg='#f0f0f5')
        cadre_budget.grid(row=3, column=0, columnspan=3, pady=10, padx=20, sticky='ew')

        # Police pour les montants
        police_mono = tkfont.Font(family='Consolas', size=13, weight='bold')

        # Label du total des dépenses
        self.label_total = Label(cadre_budget, text="Total dépensé : 0.00 €",
                                 font=police_mono, bg='#f0f0f5', fg='#c0392b')
        self.label_total.pack(side=LEFT, padx=20)

        # Label du budget restant
        self.label_restant = Label(cadre_budget, text="Budget restant : 1000.00 €",
                                   font=police_mono, bg='#f0f0f5', fg='#27ae60')
        self.label_restant.pack(side=RIGHT, padx=20)

        # ----- Bouton de suppression en bas -----
        self.bouton_supprimer = ttk.Button(root, text="🗑️ Supprimer la dépense sélectionnée",
                                           command=self.supprimer)
        self.bouton_supprimer.grid(row=4, column=0, columnspan=3, pady=10)

        # Configuration du redimensionnement des lignes/colonnes
        root.columnconfigure(0, weight=1)
        root.rowconfigure(2, weight=1)   # Le tableau s'étire verticalement
        cadre_saisie.columnconfigure(1, weight=1)  # Les champs s'adaptent horizontalement

    # ----------------------------------------------------------------------
    def ajouter(self):
        """
        Récupère les valeurs saisies, valide, ajoute la dépense au tableau,
        met à jour le total et vérifie le dépassement du budget.
        """
        # Récupération des données des champs
        desc = self.desc.get().strip()
        montant_str = self.montant.get().strip()
        cat = self.cat.get()

        # Vérification que les champs obligatoires sont remplis
        if not desc or not montant_str:
            messagebox.showerror("Erreur de saisie",
                                 "Veuillez remplir la description et le montant.")
            return

        # Conversion du montant en nombre flottant avec gestion d'erreur
        try:
            montant = float(montant_str)
        except ValueError:
            messagebox.showerror("Erreur", "Le montant doit être un nombre valide (ex: 12.50).")
            return

        # Vérification que le montant est positif
        if montant <= 0:
            messagebox.showerror("Erreur", "Le montant doit être supérieur à zéro.")
            return

        # Mise à jour du total
        self.total += montant

        # Insertion de la nouvelle ligne dans le tableau (à la fin)
        self.table.insert("", END, values=(desc, f"{montant:.2f}", cat))

        # Mise à jour des labels de total et de budget restant
        self.label_total.config(text=f"Total dépensé : {self.total:.2f} €",
                                fg='#c0392b')  # rouge pour le total
        restant = self.budget - self.total
        self.label_restant.config(text=f"Budget restant : {restant:.2f} €")

        # Changement de couleur du budget restant selon la situation
        if restant < 0:
            self.label_restant.config(fg='#e74c3c')  # rouge vif si dépassement
            messagebox.showwarning("Alerte budget",
                                   "Attention : vous avez dépassé le budget !")
        elif restant <= self.budget * 0.2:
            self.label_restant.config(fg='#f39c12')  # orange si moins de 20% restant
        else:
            self.label_restant.config(fg='#27ae60')  # vert sinon

        # Réinitialisation des champs de saisie
        self.desc.delete(0, END)
        self.montant.delete(0, END)
        self.cat.current(0)  # remet la catégorie par défaut

    # ----------------------------------------------------------------------
    def supprimer(self):
        """
        Supprime la ligne sélectionnée dans le tableau, met à jour le total
        et les informations de budget.
        """
        # Récupération de la ligne sélectionnée
        selection = self.table.selection()
        if not selection:
            messagebox.showinfo("Aucune sélection",
                                "Veuillez sélectionner une dépense à supprimer.")
            return

        # Récupération du montant de la ligne sélectionnée (2e colonne)
        valeurs = self.table.item(selection)["values"]   # ex: ('Desc', '12.50', 'Cat')
        montant_str = valeurs[1]                         # montant formaté en chaîne
        montant = float(montant_str)                     # conversion

        # Soustraction du montant au total
        self.total -= montant

        # Suppression de la ligne dans le tableau
        self.table.delete(selection)

        # Mise à jour des labels
        self.label_total.config(text=f"Total dépensé : {self.total:.2f} €",
                                fg='#c0392b')
        restant = self.budget - self.total
        self.label_restant.config(text=f"Budget restant : {restant:.2f} €")

        # Adaptation de la couleur du budget restant
        if restant < 0:
            self.label_restant.config(fg='#e74c3c')
        elif restant <= self.budget * 0.2:
            self.label_restant.config(fg='#f39c12')
        else:
            self.label_restant.config(fg='#27ae60')


# =========================================================================
# Point d'entrée de l'application
if __name__ == "__main__":
    # Création de la fenêtre racine Tk
    root = Tk()
    # Instanciation de l'application
    app = DepenseApp(root)
    # Lancement de la boucle principale d'événements
    root.mainloop()