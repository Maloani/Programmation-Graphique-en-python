import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard IA Connecté")
        self.resize(1100, 600)

        # 🔹 Connexion DB
        self.conn = sqlite3.connect("app.db")
        self.cursor = self.conn.cursor()

        # 🔹 Initialisation DB (IMPORTANT)
        self.init_db()

        # 🔹 Charger interface
        self.initUI()

    # 🔥 Création tables + données test
    def init_db(self):
        # Table présences
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS presences(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT,
        postnom TEXT,
        date TEXT
        )
        """)

        # Table dépenses
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS depenses(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        montant REAL,
        categorie TEXT
        )
        """)

        # 🔹 Vérifier si vide → insérer données test
        self.cursor.execute("SELECT COUNT(*) FROM presences")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO presences(nom, postnom, date) VALUES('Georges','Maloani','2026-01-01')")
            self.cursor.execute("INSERT INTO presences(nom, postnom, date) VALUES('Sarah','Kabila','2026-01-02')")

        self.cursor.execute("SELECT COUNT(*) FROM depenses")
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO depenses(description, montant, categorie) VALUES('Transport',100,'Transport')")
            self.cursor.execute("INSERT INTO depenses(description, montant, categorie) VALUES('Nourriture',200,'Nourriture')")
            self.cursor.execute("INSERT INTO depenses(description, montant, categorie) VALUES('Santé',80,'Santé')")

        self.conn.commit()

    # 🎨 Interface principale
    def initUI(self):
        main_layout = QHBoxLayout()

        # 🔹 SIDEBAR
        sidebar = QFrame()
        sidebar.setStyleSheet("background:#0F172A; color:white;")
        sidebar.setFixedWidth(220)

        side_layout = QVBoxLayout()
        title = QLabel("MS APP")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        side_layout.addWidget(title)

        for item in ["🏠 Dashboard", "👥 Présences", "💰 Dépenses"]:
            btn = QPushButton(item)
            btn.setStyleSheet("""
                QPushButton {
                    background:#1E293B;
                    color:white;
                    padding:10px;
                    border:none;
                    text-align:left;
                }
                QPushButton:hover {
                    background:#2563EB;
                }
            """)
            side_layout.addWidget(btn)

        side_layout.addStretch()
        sidebar.setLayout(side_layout)

        # 🔹 CONTENU
        content = QFrame()
        content.setStyleSheet("background:#F1F5F9;")
        content_layout = QVBoxLayout()

        header = QLabel("Dashboard Intelligent")
        header.setFont(QFont("Arial", 22, QFont.Bold))
        content_layout.addWidget(header)

        # 🔥 Charger données dynamiques
        nb_presences = self.get_presences()
        total_depenses = self.get_depenses()
        budget = 1000
        reste = budget - total_depenses

        # 🔹 CARTES
        cards_layout = QHBoxLayout()

        stats = [
            ("Présences", str(nb_presences)),
            ("Dépenses", f"{total_depenses} USD"),
            ("Budget restant", f"{reste} USD")
        ]

        for title, value in stats:
            card = QFrame()
            card.setStyleSheet("background:white; border-radius:10px;")
            card.setFixedSize(200, 100)

            layout = QVBoxLayout()
            lbl_title = QLabel(title)
            lbl_title.setStyleSheet("color:#64748B;")

            lbl_value = QLabel(value)
            lbl_value.setFont(QFont("Arial", 16, QFont.Bold))
            lbl_value.setStyleSheet("color:#2563EB;")

            layout.addWidget(lbl_title)
            layout.addWidget(lbl_value)

            card.setLayout(layout)
            cards_layout.addWidget(card)

        content_layout.addLayout(cards_layout)

        # 🔹 GRAPHIQUE
        categories, valeurs = self.get_depenses_par_categorie()

        fig, ax = plt.subplots()
        ax.bar(categories, valeurs)
        ax.set_title("Analyse des dépenses")

        canvas = FigureCanvas(fig)
        content_layout.addWidget(canvas)

        content.setLayout(content_layout)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)
        self.setLayout(main_layout)

    # 📊 DATA
    def get_presences(self):
        self.cursor.execute("SELECT COUNT(*) FROM presences")
        return self.cursor.fetchone()[0]

    def get_depenses(self):
        self.cursor.execute("SELECT SUM(montant) FROM depenses")
        result = self.cursor.fetchone()[0]
        return result if result else 0

    def get_depenses_par_categorie(self):
        self.cursor.execute("""
        SELECT categorie, SUM(montant)
        FROM depenses
        GROUP BY categorie
        """)
        data = self.cursor.fetchall()

        categories = [row[0] for row in data]
        valeurs = [row[1] for row in data]

        return categories, valeurs


# 🚀 LANCEMENT
app = QApplication(sys.argv)
window = Dashboard()
window.show()
sys.exit(app.exec_())