# -*- coding: utf-8 -*-

import sys
import sqlite3
# Importation des widgets PyQt5 nécessaires
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QFont, QIcon

# --------------------------------------------------------------------
# Connexion à la base de données SQLite
# --------------------------------------------------------------------
conn = sqlite3.connect("presence.db")       # Création/ouverture du fichier local
cursor = conn.cursor()                      # Curseur pour exécuter les requêtes

# Création de la table si elle n'existe pas déjà
cursor.execute("""
CREATE TABLE IF NOT EXISTS presences(
    id INTEGER PRIMARY KEY AUTOINCREMENT,   -- Identifiant unique auto-incrémenté
    nom TEXT,                               -- Nom de l'étudiant
    postnom TEXT,                           -- Postnom
    prenom TEXT,                            -- Prénom
    sexe TEXT,                              -- Sexe (Homme/Femme)
    departement TEXT,                       -- Département académique
    option TEXT,                            -- Option ou filière
    niveau TEXT,                            -- Niveau d'études
    date TEXT                               -- Date de l'enregistrement (format aaaa-mm-jj)
)
""")
conn.commit()                               # Validation immédiate de la création


# --------------------------------------------------------------------
# Classe principale de l'application
# --------------------------------------------------------------------
class PresenceApp(QMainWindow):             # Héritage de QMainWindow pour avoir barre d'état, etc.
    def __init__(self):
        super().__init__()                  # Appel du constructeur parent
        self.setWindowTitle("📋 Gestion de Présence Intelligente")
        self.resize(1050, 650)              # Taille de la fenêtre (largeur x hauteur)

        # ----- Feuille de style globale pour un design moderne -----
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QGroupBox {
                font: bold 14px 'Segoe UI';
                color: #2c3e50;
                border: 1px solid #dcdde1;
                border-radius: 8px;
                margin-top: 14px;
                padding-top: 20px;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
            }
            QLabel {
                font: 12px 'Segoe UI';
                color: #34495e;
            }
            QLineEdit {
                font: 12px 'Segoe UI';
                padding: 8px;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
            }
            QComboBox {
                font: 12px 'Segoe UI';
                padding: 6px;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                background-color: #ffffff;
            }
            QPushButton {
                font: bold 12px 'Segoe UI';
                padding: 10px 16px;
                border-radius: 6px;
                color: white;
                background-color: #3498db;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QTableWidget {
                font: 12px 'Segoe UI';
                background-color: #ffffff;
                alternate-background-color: #f0f4f8;
                gridline-color: #dcdde1;
                border: 1px solid #dcdde1;
                border-radius: 5px;
                selection-background-color: #3498db;
                selection-color: white;
            }
            QHeaderView::section {
                background-color: #ecf0f1;
                font: bold 12px 'Segoe UI';
                padding: 6px;
                border: 1px solid #dcdde1;
            }
            QStatusBar {
                font: 11px 'Segoe UI';
                color: #555;
            }
        """)

        # ----- Widget central et layout principal -----
        central = QWidget()                  # Conteneur central du QMainWindow
        self.setCentralWidget(central)       # Assignation du widget central
        main_layout = QVBoxLayout(central)   # Layout vertical principal
        main_layout.setContentsMargins(20, 20, 20, 20)  # Marges globales
        main_layout.setSpacing(12)           # Espacement entre les widgets

        # ----- Groupe formulaire de saisie -----
        form_group = QGroupBox("👤 Informations de l'étudiant")
        form_layout = QGridLayout(form_group)  # Grille pour organiser les champs
        form_layout.setSpacing(12)

        # Création des champs de saisie
        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Entrez le nom")       # Texte indicatif
        self.postnom = QLineEdit()
        self.postnom.setPlaceholderText("Entrez le postnom")
        self.prenom = QLineEdit()
        self.prenom.setPlaceholderText("Entrez le prénom")

        self.sexe = QComboBox()
        self.sexe.addItems(["Homme", "Femme"])              # Choix du sexe

        self.departement = QLineEdit()
        self.departement.setPlaceholderText("Ex: Informatique")
        self.option = QLineEdit()
        self.option.setPlaceholderText("Ex: Génie Logiciel")

        self.niveau = QComboBox()
        self.niveau.addItems(["Master 1", "Master 2", "PhD I", "PhD II", "PhD III"])
        self.niveau.setCurrentIndex(0)                      # Sélection par défaut

        # Placement des labels et champs dans la grille (ligne, colonne)
        form_layout.addWidget(QLabel("Nom"), 0, 0)
        form_layout.addWidget(self.nom, 0, 1)
        form_layout.addWidget(QLabel("Postnom"), 0, 2)
        form_layout.addWidget(self.postnom, 0, 3)

        form_layout.addWidget(QLabel("Prénom"), 1, 0)
        form_layout.addWidget(self.prenom, 1, 1)
        form_layout.addWidget(QLabel("Sexe"), 1, 2)
        form_layout.addWidget(self.sexe, 1, 3)

        form_layout.addWidget(QLabel("Département"), 2, 0)
        form_layout.addWidget(self.departement, 2, 1)
        form_layout.addWidget(QLabel("Option"), 2, 2)
        form_layout.addWidget(self.option, 2, 3)

        form_layout.addWidget(QLabel("Niveau"), 3, 0)
        form_layout.addWidget(self.niveau, 3, 1)

        main_layout.addWidget(form_group)    # Ajout du groupe formulaire au layout principal

        # ----- Boutons d'action -----
        btn_layout = QHBoxLayout()           # Layout horizontal pour les boutons
        btn_layout.setSpacing(15)

        self.btn_add = QPushButton("✅ Marquer Présence")
        self.btn_add.setCursor(Qt.PointingHandCursor)  # Curseur main au survol
        self.btn_add.clicked.connect(self.ajouter)     # Connexion du clic à la méthode

        self.btn_refresh = QPushButton("🔄 Afficher Historique")
        self.btn_refresh.setCursor(Qt.PointingHandCursor)
        self.btn_refresh.clicked.connect(self.afficher)

        self.btn_delete = QPushButton("🗑️ Supprimer la sélection")
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_delete.clicked.connect(self.supprimer)

        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()              # Espace extensible pousse les boutons vers la gauche
        main_layout.addLayout(btn_layout)

        # ----- Tableau des présences -----
        self.table = QTableWidget()
        self.table.setColumnCount(8)         # 8 colonnes
        self.table.setHorizontalHeaderLabels([
            "Nom", "Postnom", "Prénom", "Sexe",
            "Département", "Option", "Niveau", "Date"
        ])
        self.table.setAlternatingRowColors(True)   # Couleurs alternées pour les lignes
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # Sélection par ligne entière
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)   # Lecture seule
        self.table.horizontalHeader().setStretchLastSection(True)      # Dernière colonne étirée
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # Colonnes adaptatives
        main_layout.addWidget(self.table, stretch=1)  # Le tableau prend l'espace restant

        # ----- Barre d'état (informations) -----
        self.status_bar = self.statusBar()   # Récupération de la barre d'état
        self.status_bar.showMessage("Prêt | Base chargée", 3000)  # Message temporaire

        # Chargement initial des données
        self.afficher()

    # ------------------------------------------------------------------
    def ajouter(self):
        """Ajoute une nouvelle entrée de présence dans la base de données."""
        # Récupération des valeurs saisies
        nom = self.nom.text().strip()
        postnom = self.postnom.text().strip()
        prenom = self.prenom.text().strip()
        sexe = self.sexe.currentText()
        departement = self.departement.text().strip()
        option = self.option.text().strip()
        niveau = self.niveau.currentText()

        # Vérification des champs obligatoires
        if not nom or not postnom or not prenom or not departement or not option:
            QMessageBox.warning(self, "Erreur de saisie",
                                "Tous les champs textuels sont obligatoires.\nVeuillez les compléter.")
            return

        # Date du jour au format ISO
        date = QDateTime.currentDateTime().toString("yyyy-MM-dd")

        # Vérification anti-doublon : même personne et même date
        cursor.execute("""
        SELECT * FROM presences WHERE nom=? AND postnom=? AND date=?
        """, (nom, postnom, date))
        if cursor.fetchone():
            QMessageBox.warning(self, "Doublon détecté",
                                "Cette personne a déjà été enregistrée aujourd'hui.")
            return

        # Insertion dans la base de données
        cursor.execute("""
        INSERT INTO presences(nom, postnom, prenom, sexe, departement, option, niveau, date)
        VALUES(?,?,?,?,?,?,?,?)
        """, (nom, postnom, prenom, sexe, departement, option, niveau, date))
        conn.commit()

        # Message de succès dans la barre d'état
        self.status_bar.showMessage(f"✔ Présence de {prenom} {nom} ajoutée avec succès", 5000)

        # Rafraîchissement du tableau
        self.afficher()

    # ------------------------------------------------------------------
    def afficher(self):
        """Recharge toutes les données depuis la base et les affiche dans le tableau."""
        cursor.execute(
            "SELECT nom, postnom, prenom, sexe, departement, option, niveau, date FROM presences"
        )
        data = cursor.fetchall()             # Liste de tuples contenant toutes les lignes

        self.table.setRowCount(len(data))    # Fixe le nombre de lignes du tableau

        for i, row in enumerate(data):       # Parcourt chaque ligne récupérée
            for j, val in enumerate(row):    # Parcourt chaque colonne de la ligne
                item = QTableWidgetItem(str(val))   # Crée un élément de tableau
                item.setTextAlignment(Qt.AlignCenter)  # Centrage du texte
                self.table.setItem(i, j, item)

        # Mise à jour du message de la barre d'état avec le nombre d'enregistrements
        self.status_bar.showMessage(f"📊 {len(data)} enregistrement(s) affiché(s)", 3000)

    # ------------------------------------------------------------------
    def supprimer(self):
        """Supprime la ligne sélectionnée du tableau et de la base de données."""
        selected_row = self.table.currentRow()   # Index de la ligne sélectionnée
        if selected_row == -1:                   # Aucune ligne sélectionnée
            QMessageBox.information(self, "Aucune sélection",
                                    "Veuillez d'abord sélectionner une ligne à supprimer.")
            return

        # Récupération des identifiants de la ligne (nom, postnom, date)
        nom = self.table.item(selected_row, 0).text()
        postnom = self.table.item(selected_row, 1).text()
        date = self.table.item(selected_row, 7).text()

        # Demande de confirmation
        reponse = QMessageBox.question(
            self, "Confirmation de suppression",
            f"Supprimer définitivement la présence de {nom} {postnom} du {date} ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reponse != QMessageBox.Yes:
            return

        # Suppression dans la base via les critères uniques (nom, postnom, date)
        cursor.execute(
            "DELETE FROM presences WHERE nom=? AND postnom=? AND date=?",
            (nom, postnom, date)
        )
        conn.commit()

        # Suppression de la ligne visuelle dans le tableau
        self.table.removeRow(selected_row)

        # Barre d'état
        self.status_bar.showMessage(f"❌ Présence de {nom} supprimée", 5000)


# ======================================================================
# Point d'entrée de l'application
# ======================================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)             # Création de l'application Qt
    app.setFont(QFont("Segoe UI", 10))       # Police par défaut pour toute l'application
    window = PresenceApp()                   # Instanciation de la fenêtre principale
    window.show()                            # Affichage de la fenêtre
    sys.exit(app.exec_())                    # Boucle d'événements et sortie propre