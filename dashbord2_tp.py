# -*- coding: utf-8 -*-

import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtGui import QFont, QIcon
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# ======================== BASE DE DONNÉES ==============================
# Connexion (ou création) du fichier de base pour les présences
presence_conn = sqlite3.connect("presence.db")
presence_cursor = presence_conn.cursor()
presence_cursor.execute("""
CREATE TABLE IF NOT EXISTS presences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT, postnom TEXT, prenom TEXT, sexe TEXT,
    departement TEXT, option TEXT, niveau TEXT, date TEXT
)
""")
presence_conn.commit()

# Connexion pour les dépenses
depense_conn = sqlite3.connect("depenses.db")
depense_cursor = depense_conn.cursor()
depense_cursor.execute("""
CREATE TABLE IF NOT EXISTS depenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT, montant REAL, categorie TEXT, date TEXT
)
""")
depense_conn.commit()

# ======================== PAGE PRÉSENCES (TP1) =========================
class PresencePage(QWidget):
    """Widget de gestion des présences, intégrable dans un QStackedWidget."""
    def __init__(self):
        super().__init__()
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # ---- Formulaire ----
        form_group = QGroupBox("👤 Nouvelle présence")
        form_group.setStyleSheet("QGroupBox{font: bold 14px;}")
        form_layout = QGridLayout(form_group)
        form_layout.setSpacing(10)

        # Champs de saisie
        self.nom = QLineEdit()
        self.nom.setPlaceholderText("Nom")
        self.postnom = QLineEdit()
        self.postnom.setPlaceholderText("Postnom")
        self.prenom = QLineEdit()
        self.prenom.setPlaceholderText("Prénom")
        self.sexe = QComboBox()
        self.sexe.addItems(["Homme", "Femme"])
        self.departement = QLineEdit()
        self.departement.setPlaceholderText("Département")
        self.option = QLineEdit()
        self.option.setPlaceholderText("Option")
        self.niveau = QComboBox()
        self.niveau.addItems(["Master 1", "Master 2", "PhD I", "PhD II", "PhD III"])
        self.niveau.setCurrentIndex(0)

        # Placement dans la grille
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

        main_layout.addWidget(form_group)

        # Boutons actions
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("✅ Marquer présence")
        self.btn_add.clicked.connect(self.ajouter)
        self.btn_refresh = QPushButton("🔄 Rafraîchir")
        self.btn_refresh.clicked.connect(self.afficher)
        self.btn_delete = QPushButton("🗑️ Supprimer sélection")
        self.btn_delete.clicked.connect(self.supprimer)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        # Tableau des présences
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(
            ["Nom", "Postnom", "Prénom", "Sexe", "Département", "Option", "Niveau", "Date"]
        )
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        # Chargement initial des données
        self.afficher()

    def ajouter(self):
        """Ajoute une présence après validation."""
        nom = self.nom.text().strip()
        postnom = self.postnom.text().strip()
        prenom = self.prenom.text().strip()
        sexe = self.sexe.currentText()
        departement = self.departement.text().strip()
        option = self.option.text().strip()
        niveau = self.niveau.currentText()

        if not nom or not postnom or not prenom or not departement or not option:
            QMessageBox.warning(self, "Erreur", "Tous les champs obligatoires doivent être remplis.")
            return

        date = QDateTime.currentDateTime().toString("yyyy-MM-dd")
        # Vérification doublon
        presence_cursor.execute(
            "SELECT * FROM presences WHERE nom=? AND postnom=? AND date=?",
            (nom, postnom, date)
        )
        if presence_cursor.fetchone():
            QMessageBox.warning(self, "Doublon", "Présence déjà enregistrée aujourd'hui.")
            return

        presence_cursor.execute(
            "INSERT INTO presences VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)",
            (nom, postnom, prenom, sexe, departement, option, niveau, date)
        )
        presence_conn.commit()
        self.afficher()  # rafraîchir

    def afficher(self):
        """Recharge toutes les présences dans le tableau."""
        presence_cursor.execute(
            "SELECT nom, postnom, prenom, sexe, departement, option, niveau, date FROM presences"
        )
        rows = presence_cursor.fetchall()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)

    def supprimer(self):
        """Supprime la présence sélectionnée après confirmation."""
        current = self.table.currentRow()
        if current < 0:
            QMessageBox.information(self, "Info", "Sélectionnez une ligne à supprimer.")
            return
        nom = self.table.item(current, 0).text()
        postnom = self.table.item(current, 1).text()
        date = self.table.item(current, 7).text()
        confirm = QMessageBox.question(
            self, "Confirmation",
            f"Supprimer la présence de {nom} {postnom} le {date} ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            presence_cursor.execute(
                "DELETE FROM presences WHERE nom=? AND postnom=? AND date=?",
                (nom, postnom, date)
            )
            presence_conn.commit()
            self.afficher()

# ======================== PAGE DÉPENSES (TP2) ========================== 
class DepensePage(QWidget):
    """Widget de gestion des dépenses, équivalent PyQt5 de l'application Tkinter."""
    def __init__(self):
        super().__init__()
        self.total = 0.0               # Cumul des dépenses
        self.budget = 1000.0           # Budget maximal

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # ---- Formulaire ----
        form_group = QGroupBox("💰 Nouvelle dépense")
        form_layout = QGridLayout(form_group)
        form_layout.setSpacing(10)

        self.desc = QLineEdit()
        self.desc.setPlaceholderText("Description")
        self.montant = QLineEdit()
        self.montant.setPlaceholderText("Montant (€)")
        self.categorie = QComboBox()
        self.categorie.addItems(["Transport", "Nourriture", "Santé", "Loisirs", "Logement", "Autres"])

        form_layout.addWidget(QLabel("Description"), 0, 0)
        form_layout.addWidget(self.desc, 0, 1)
        form_layout.addWidget(QLabel("Montant"), 0, 2)
        form_layout.addWidget(self.montant, 0, 3)
        form_layout.addWidget(QLabel("Catégorie"), 1, 0)
        form_layout.addWidget(self.categorie, 1, 1)

        main_layout.addWidget(form_group)

        # Boutons
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("➕ Ajouter")
        self.btn_add.clicked.connect(self.ajouter)
        self.btn_supprimer = QPushButton("🗑️ Supprimer sélection")
        self.btn_supprimer.clicked.connect(self.supprimer)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_supprimer)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Description", "Montant (€)", "Catégorie", "Date"])
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        main_layout.addWidget(self.table)

        # Zone budget
        budget_layout = QHBoxLayout()
        self.lbl_total = QLabel("Total dépensé : 0.00 €")
        self.lbl_total.setStyleSheet("font-weight:bold; color:#c0392b;")
        self.lbl_restant = QLabel("Budget restant : 1000.00 €")
        self.lbl_restant.setStyleSheet("font-weight:bold; color:#27ae60;")
        budget_layout.addWidget(self.lbl_total)
        budget_layout.addStretch()
        budget_layout.addWidget(self.lbl_restant)
        main_layout.addLayout(budget_layout)

        self.afficher()

    def ajouter(self):
        desc = self.desc.text().strip()
        montant_str = self.montant.text().strip()
        cat = self.categorie.currentText()

        if not desc or not montant_str:
            QMessageBox.warning(self, "Erreur", "Description et montant obligatoires.")
            return
        try:
            montant = float(montant_str)
        except ValueError:
            QMessageBox.warning(self, "Erreur", "Le montant doit être un nombre.")
            return
        if montant <= 0:
            QMessageBox.warning(self, "Erreur", "Le montant doit être positif.")
            return

        date = QDateTime.currentDateTime().toString("yyyy-MM-dd")
        depense_cursor.execute(
            "INSERT INTO depenses (description, montant, categorie, date) VALUES (?, ?, ?, ?)",
            (desc, montant, cat, date)
        )
        depense_conn.commit()
        self.afficher()
        self.desc.clear()
        self.montant.clear()

    def afficher(self):
        depense_cursor.execute("SELECT description, montant, categorie, date FROM depenses")
        rows = depense_cursor.fetchall()
        self.table.setRowCount(len(rows))
        total = 0.0
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                if j == 1:  # montant formaté
                    item = QTableWidgetItem(f"{val:.2f}")
                    total += val
                else:
                    item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, j, item)

        self.total = total
        self.lbl_total.setText(f"Total dépensé : {total:.2f} €")
        restant = self.budget - total
        self.lbl_restant.setText(f"Budget restant : {restant:.2f} €")
        # Couleurs conditionnelles
        if restant < 0:
            self.lbl_restant.setStyleSheet("font-weight:bold; color:#e74c3c;")
            QMessageBox.warning(self, "Alerte", "Budget dépassé !")
        elif restant <= self.budget * 0.2:
            self.lbl_restant.setStyleSheet("font-weight:bold; color:#f39c12;")
        else:
            self.lbl_restant.setStyleSheet("font-weight:bold; color:#27ae60;")

    def supprimer(self):
        current = self.table.currentRow()
        if current < 0:
            QMessageBox.information(self, "Info", "Sélectionnez une ligne.")
            return
        desc = self.table.item(current, 0).text()
        montant = float(self.table.item(current, 1).text())
        cat = self.table.item(current, 2).text()
        date = self.table.item(current, 3).text()
        confirm = QMessageBox.question(self, "Confirmation", f"Supprimer la dépense « {desc} » ?",
                                      QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            depense_cursor.execute(
                "DELETE FROM depenses WHERE description=? AND montant=? AND categorie=? AND date=?",
                (desc, montant, cat, date)
            )
            depense_conn.commit()
            self.afficher()

# ======================== PAGE STATISTIQUES (GRAPHIQUE) =================
class StatsPage(QWidget):
    """Page affichant un graphique des dépenses par catégorie."""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.charger_graphique()

    def charger_graphique(self):
        """Charge les données depuis la base et trace un diagramme en barres."""
        depense_cursor.execute("SELECT categorie, SUM(montant) FROM depenses GROUP BY categorie")
        data = depense_cursor.fetchall()
        categories = [row[0] for row in data]
        valeurs = [row[1] for row in data]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(categories, valeurs, color='#3498db')
        ax.set_title("Répartition des dépenses par catégorie", fontweight='bold')
        ax.set_ylabel("Montant (€)")
        self.canvas.draw()

# ======================== FENÊTRE PRINCIPALE ===========================
class MainWindow(QMainWindow):
    """Fenêtre principale avec sidebar et pages multiples."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📊 Dashboard IA – Gestion intégrée")
        self.resize(1200, 700)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ---- Sidebar ----
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color:#0F172A;")
        sidebar.setFixedWidth(220)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(10, 20, 10, 20)
        sidebar_layout.setSpacing(8)

        # Logo / Titre
        title = QLabel("MS APP")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setStyleSheet("color:white;")
        title.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title)

        # Boutons de navigation
        self.buttons = {}
        pages = {
            "🏠 Dashboard": 0,
            "👥 Présences": 1,
            "💰 Dépenses": 2,
            "📊 Statistiques": 3,
            "⚙ Paramètres": 4
        }
        for text, idx in pages.items():
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color:#1E293B;
                    color:white;
                    padding:12px;
                    text-align:left;
                    border:none;
                    border-radius:6px;
                    font: 12px 'Segoe UI';
                }
                QPushButton:hover {
                    background-color:#2563EB;
                }
            """)
            btn.clicked.connect(lambda checked, index=idx: self.switch_page(index))
            sidebar_layout.addWidget(btn)
            self.buttons[text] = btn

        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar)

        # ---- Zone de contenu (QStackedWidget) ----
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color:#F1F5F9;")

        # Page 0 : Dashboard d'accueil
        self.page_dashboard = self.create_dashboard_page()
        self.stack.addWidget(self.page_dashboard)

        # Page 1 : Présences (TP1)
        self.page_presence = PresencePage()
        self.stack.addWidget(self.page_presence)

        # Page 2 : Dépenses (TP2)
        self.page_depense = DepensePage()
        self.stack.addWidget(self.page_depense)

        # Page 3 : Statistiques (graphique actualisable)
        self.page_stats = StatsPage()
        self.stack.addWidget(self.page_stats)

        # Page 4 : Paramètres (placeholder)
        self.page_settings = QLabel("⚙ Page des paramètres (à implémenter)")
        self.page_settings.setAlignment(Qt.AlignCenter)
        self.page_settings.setFont(QFont("Segoe UI", 16))
        self.stack.addWidget(self.page_settings)

        main_layout.addWidget(self.stack)

        # Page active par défaut
        self.stack.setCurrentIndex(0)

    def switch_page(self, index):
        """Change la page affichée dans le QStackedWidget."""
        self.stack.setCurrentIndex(index)
        # Si on va sur la page statistiques, on rafraîchit le graphique
        if index == 3:
            self.page_stats.charger_graphique()

    def create_dashboard_page(self):
        """Crée la page d'accueil avec cartes et graphique."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # En-tête
        header = QLabel("Tableau de bord")
        header.setFont(QFont("Segoe UI", 24, QFont.Bold))
        header.setStyleSheet("color:#0F172A;")
        layout.addWidget(header)

        # Cartes statistiques
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # Récupération des valeurs dynamiques
        presence_cursor.execute("SELECT COUNT(*) FROM presences")
        nb_presences = presence_cursor.fetchone()[0]
        depense_cursor.execute("SELECT SUM(montant) FROM depenses")
        total_dep = depense_cursor.fetchone()[0] or 0.0
        budget_restant = 1000.0 - total_dep

        stats_data = [
            ("Présences", str(nb_presences)),
            ("Dépenses", f"{total_dep:.0f} €"),
            ("Budget restant", f"{budget_restant:.0f} €"),
            ("Étudiants", "80")  # peut être dynamisé si besoin
        ]

        for title_text, value in stats_data:
            card = QFrame()
            card.setStyleSheet("background:white; border-radius:12px; padding:15px;")
            card.setFixedSize(180, 100)
            vbox = QVBoxLayout(card)
            lbl_titre = QLabel(title_text)
            lbl_titre.setStyleSheet("color:#64748B; font-size:12px;")
            lbl_val = QLabel(value)
            lbl_val.setFont(QFont("Segoe UI", 18, QFont.Bold))
            lbl_val.setStyleSheet("color:#2563EB;")
            vbox.addWidget(lbl_titre)
            vbox.addWidget(lbl_val)
            cards_layout.addWidget(card)

        cards_layout.addStretch()
        layout.addLayout(cards_layout)

        # Graphique rapide des dépenses
        fig, ax = plt.subplots()
        depense_cursor.execute("SELECT categorie, SUM(montant) FROM depenses GROUP BY categorie")
        data = depense_cursor.fetchall()
        if data:
            cats = [r[0] for r in data]
            vals = [r[1] for r in data]
            ax.bar(cats, vals, color='#3498db')
            ax.set_title("Aperçu des dépenses", fontweight='bold')
            ax.set_ylabel("€")
        else:
            ax.text(0.5, 0.5, 'Aucune dépense enregistrée', ha='center', va='center')
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)

        return page

# ======================== LANCEMENT ====================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    # Feuille de style globale pour finaliser le design
    app.setStyleSheet("""
        QGroupBox {
            font: bold 13px;
            border: 1px solid #dcdde1;
            border-radius: 8px;
            margin-top: 10px;
            padding-top: 20px;
            background: white;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 15px;
            padding: 0 6px;
        }
        QLineEdit, QComboBox {
            padding: 8px;
            border: 1px solid #dcdde1;
            border-radius: 5px;
            background: white;
        }
        QLineEdit:focus {
            border-color: #3498db;
        }
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 18px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QTableWidget {
            background: white;
            gridline-color: #dcdde1;
            border: 1px solid #dcdde1;
            border-radius: 5px;
        }
        QHeaderView::section {
            background: #ecf0f1;
            font-weight: bold;
            padding: 6px;
            border: 1px solid #dcdde1;
        }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())