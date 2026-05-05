# =========================================
# IMPORTATIONS
# =========================================

import sys   # Gestion système
import random   # Simulation IA trafic

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
)

from PyQt5.QtChart import QChart, QChartView, QLineSeries   # Graphiques
from PyQt5.QtCore import QTimer   # Animation temps réel

# =========================================
# CLASSE CARTE STATISTIQUE
# =========================================

class Carte(QFrame):
    def __init__(self, titre, valeur):
        super().__init__()

        self.setFixedSize(180, 100)   # Taille carte

        # Style carte
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
            }
        """)

        layout = QVBoxLayout()

        self.titre = QLabel(titre)   # Titre
        self.titre.setStyleSheet("color: gray;")

        self.valeur = QLabel(str(valeur))   # Valeur dynamique
        self.valeur.setStyleSheet("font-size:20px; font-weight:bold;")

        layout.addWidget(self.titre)
        layout.addWidget(self.valeur)

        self.setLayout(layout)

    # Fonction pour mettre à jour la valeur
    def update_value(self, val):
        self.valeur.setText(str(val))

# =========================================
# DASHBOARD PRINCIPAL
# =========================================

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Dashboard IA Trafic - MS Trans")
        self.setGeometry(100, 100, 900, 600)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout()

        # =========================================
        # TITRE
        # =========================================

        title = QLabel("📊 Dashboard IA Trafic")
        title.setStyleSheet("font-size:24px; font-weight:bold;")
        main_layout.addWidget(title)

        # =========================================
        # CARTES STATISTIQUES
        # =========================================

        cards_layout = QHBoxLayout()

        self.carte_vehicules = Carte("🚗 Véhicules", 0)
        self.carte_vitesse = Carte("⚡ Vitesse Moyenne", 0)
        self.carte_trafic = Carte("📈 Niveau Trafic", 0)
        self.carte_alertes = Carte("⚠ Alertes", 0)

        cards_layout.addWidget(self.carte_vehicules)
        cards_layout.addWidget(self.carte_vitesse)
        cards_layout.addWidget(self.carte_trafic)
        cards_layout.addWidget(self.carte_alertes)

        main_layout.addLayout(cards_layout)

        # =========================================
        # GRAPHIQUE IA TRAFIC
        # =========================================

        self.series = QLineSeries()   # Série de données

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Évolution du trafic en temps réel")

        self.chart.createDefaultAxes()

        self.chart_view = QChartView(self.chart)

        main_layout.addWidget(self.chart_view)

        # =========================================
        # BOUTON ACTIVER IA
        # =========================================

        self.btn_start = QPushButton("▶ Lancer Simulation IA")
        self.btn_start.clicked.connect(self.start_simulation)

        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #2563EB;
                color: white;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #1D4ED8;
            }
        """)

        main_layout.addWidget(self.btn_start)

        central.setLayout(main_layout)

        # =========================================
        # TIMER POUR SIMULATION TEMPS REEL
        # =========================================

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)

        self.x = 0   # Axe X du graphique

    # =========================================
    # DEMARRER SIMULATION IA
    # =========================================

    def start_simulation(self):
        self.timer.start(1000)   # Mise à jour chaque seconde

    # =========================================
    # MISE A JOUR DES DONNEES (IA SIMULÉE)
    # =========================================

    def update_data(self):

        # Simulation IA trafic
        vehicules = random.randint(50, 200)
        vitesse = random.randint(20, 80)
        trafic = random.randint(1, 10)
        alertes = random.randint(0, 5)

        # Mise à jour cartes
        self.carte_vehicules.update_value(vehicules)
        self.carte_vitesse.update_value(vitesse)
        self.carte_trafic.update_value(trafic)
        self.carte_alertes.update_value(alertes)

        # Mise à jour graphique
        self.series.append(self.x, trafic)
        self.x += 1

        # Limiter taille du graphique
        if self.x > 20:
            self.series.removePoints(0, 1)

# =========================================
# LANCEMENT APPLICATION
# =========================================

app = QApplication(sys.argv)
window = Dashboard()
window.show()
sys.exit(app.exec_())