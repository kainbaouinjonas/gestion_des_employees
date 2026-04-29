# main.py
import sys
import os

# Ajoute le dossier parent (Employee_app) au chemin Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Maintenant on peut importer
from gui.app import run

if __name__ == "__main__":
    print("=" * 50)
    print("EMPLOYEE MANAGEMENT SYSTEM")
    print("=" * 50)
    print("Démarrage de l'application...")
    run()