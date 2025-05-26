
from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

app = Flask(__name__)

# Inserisci la tua connection string MongoDB come variabile ambiente
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://admin:admin123@cluster0.mfgmbey.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# Initialize MongoDB connection
client = None
db = None
collection = None

try:
    # Create a new client and connect to the server
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    
    # Send a ping to confirm a successful connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
    
    db = client["quixa"]
    collection = db["quixa_collection"]
    
except Exception as e:
    print(f"Errore connessione MongoDB: {e}")
    client = None
    db = None
    collection = None

@app.route("/", methods=["GET"])
def home():
    connection_status = "Connesso" if collection is not None else "Non connesso"
    return jsonify({
        "message": "API Quixa attiva",
        "database_status": connection_status,
        "endpoints": {
            "POST /verifica-polizza": "Verifica esistenza polizza per prefisso"
        }
    })

@app.route("/verifica-polizza", methods=["POST"])
def verifica_polizza():
    if collection is None:
        return jsonify({"errore": "Database non disponibile"}), 500
        
    data = request.get_json()
    numero_polizza = data.get("numero_polizza", "")

    if not numero_polizza:
        return jsonify({"errore": "Parametro 'numero_polizza' mancante"}), 400

    try:
        # Cerco polizza che inizia con le prime 3 cifre di numero_polizza
        prefisso = numero_polizza[:3]

        result = collection.find_one({"numero_polizza": {"$regex": f"^{prefisso}"}})

        if result:
            return jsonify({
                "esiste": True,
                "numero_polizza": result["numero_polizza"],
                "utente_id": result["utente_id"],
                "stato": result.get("stato", "")
            })
        else:
            return jsonify({"esiste": False})
            
    except Exception as e:
        return jsonify({"errore": f"Errore durante la ricerca: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
