from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# Initialisation de Flask
app = Flask(__name__)

# Activation de CORS
CORS(app)  # Permet toutes les origines. À restreindre en production.

# Connexion à MongoDB
MONGO_URI = "mongodb://localhost:27017"  # Remplacez si nécessaire
client = MongoClient(MONGO_URI)
db = client['louagisteDB']
logs_collection = db['logs']
users_collection = db['users']
tickets_collection = db['tickets']  # Ajout de la collection tickets

# Route pour récupérer les logs
@app.route('/api/logs', methods=['GET'])
def get_logs():
    try:
        # Récupérer les logs depuis MongoDB
        logs = list(logs_collection.find({}, {"_id": 0}))  # Exclure `_id` du résultat
        return jsonify(logs), 200
    except Exception as e:
        # Gestion des erreurs
        return jsonify({"error": str(e)}), 500

# Route pour créer un ticket
@app.route('/tickets', methods=['POST'])
def create_ticket():
    data = request.json
    itineraire = data.get('itineraire')
    date = data.get('date')

    if not (itineraire and date):
        return jsonify({"error": "L'itinéraire et la date sont obligatoires"}), 400

    # Ajouter le ticket à la base de données
    tickets_collection.insert_one({
        "itineraire": itineraire,
        "date": date
    })

    return jsonify({"message": "Ticket réservé avec succès"}), 201

# Route pour le signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    nom = data.get('nom')
    prenom = data.get('prenom')
    cin = data.get('cin')
    password = data.get('password')

    if not (nom and prenom and cin and password):
        return jsonify({"error": "Tous les champs sont obligatoires"}), 400

    # Vérifier si l'utilisateur existe déjà
    if users_collection.find_one({"cin": cin}):
        return jsonify({"error": "Un utilisateur avec ce CIN existe déjà"}), 409

    # Ajouter l'utilisateur à la base de données avec un mot de passe haché
    hashed_password = generate_password_hash(password)
    users_collection.insert_one({
        "nom": nom,
        "prenom": prenom,
        "cin": cin,
        "password": hashed_password
    })

    return jsonify({"message": "Utilisateur créé avec succès"}), 201

# Route pour le login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    cin = data.get('cin')
    password = data.get('password')

    if not (cin and password):
        return jsonify({"error": "CIN et mot de passe sont obligatoires"}), 400

    # Rechercher l'utilisateur par CIN
    user = users_collection.find_one({"cin": cin})
    if not user:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    # Vérifier le mot de passe
    if not check_password_hash(user['password'], password):
        return jsonify({"error": "Mot de passe incorrect"}), 401

    return jsonify({"message": f"Bienvenue {user['prenom']} {user['nom']}!"}), 200

if __name__ == '__main__':
    # Lancer l'application Flask
    app.run(debug=True, port=5000)
