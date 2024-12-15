import random
from random import randint
import time
from datetime import datetime
from pymongo import MongoClient  # Bibliothèque pour MongoDB

# Connexion à MongoDB (assurez-vous que MongoDB Compass est connecté à cette URI)
MONGO_URI = "mongodb://localhost:27017"  # Remplacez par votre URI si nécessaire
client = MongoClient(MONGO_URI)

# Nom de la base de données et de la collection
db = client['louagisteDB']  # Connexion à la base de données existante
logs_collection = db['logs']  # Nouvelle collection pour les données générées

# Liste des gouvernorats en Tunisie
gouvernorats = [
    "Ariana", "Béja", "Ben Arous", "Bizerte", "Gabès", "Gafsa", "Jendouba",
    "Kairouan", "Kasserine", "Kébili", "Le Kef", "Mahdia", "La Manouba",
    "Médenine", "Monastir", "Nabeul", "Sfax", "Sidi Bouzid", "Siliana",
    "Sousse", "Tataouine", "Tozeur", "Tunis", "Zaghouan"
]

# Générer un numéro d'immatriculation de louage aléatoire
def generate_louage_id():
    first_part = random.randint(110, 246)
    second_part = random.randint(1, 9999)
    return f"{first_part} TUN {second_part:04d}"

# Fonction de simulation du capteur
def simulate_sensor():
    while True:
        # Générer un numéro d'immatriculation pour un louage
        louage_id = generate_louage_id()
        
        # Déterminer aléatoirement si le louage entre ou sort
        action = random.choice(["entrée", "sortie"])
        
        # Choisir aléatoirement les gouvernorats de départ et de destination
        depart = random.choice(gouvernorats)
        destination = random.choice(gouvernorats)
        
        # Déterminer le texte en fonction de l'action
        if action == "entrée":
            texte = f"venu de {depart}"
        else:
            texte = f"allant à {destination}"
        
        # Créer une entrée pour le log
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "louage_id": louage_id,
            "action": action,
            "depart": depart if action == "entrée" else None,
            "destination": destination if action == "sortie" else None
        }
        
        # Afficher l'entrée
        print(f"{log_entry['timestamp']} - Louage {log_entry['louage_id']} - {log_entry['action']} ({texte})")
        
        # Insérer le log dans MongoDB (collection `logs`)
        logs_collection.insert_one(log_entry)
        
        # Pause (entre 20 et 60 secondes)
        nb = randint(20, 60)
        time.sleep(nb)

# Lancer la simulation du capteur
simulate_sensor()
